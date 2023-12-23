import abc
from concurrent.futures import Executor, ThreadPoolExecutor
from threading import Lock, Event

from .idorder import IDOrder
from .orderer import SerializableOrderer


class Stopped(Exception):
    pass


class ParallelModule(abc.ABC):
    def submit_task(self, func, *args, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def shutdown(self):
        raise NotImplementedError  # pragma: no cover

    def join(self):
        raise NotImplementedError  # pragma: no cover

    def next_value(self):
        raise NotImplementedError  # pragma: no cover


class SerializableParallelModule(ParallelModule):
    def __init__(self, max_workers: int = None):
        self._executor_value = None
        self._max_workers = max_workers

        # states
        self._current_task_id = -1
        self._retvals = {}
        self._orderer = SerializableOrderer()
        self._idorder = IDOrder()

        # global signals
        self._stop_event = Event()
        self._global_lock = Lock()

    @property
    def _executor(self) -> Executor:
        if self._executor_value is None:
            self._executor_value = ThreadPoolExecutor(max_workers=self._max_workers)
        return self._executor_value

    def _wait_for_num_from_order(self, num):
        while True:
            if self._stop_event.is_set():
                raise Stopped('Stopped. No order available.')

            if self._orderer.wait_for_num(num, timeout=1.0):
                return True

    def _func_wrapper(self, id_: int, func, *args, **kwargs):
        event = Event()

        def _new_func():
            event.set()
            if self._stop_event.is_set():
                return

            retval = func(*args, **kwargs)

            try:
                self._wait_for_num_from_order(id_)
            except Stopped:
                pass
            else:
                with self._global_lock:
                    self._retvals[id_] = retval
                    self._idorder.set_id(id_)

        return _new_func, event

    def submit_task(self, func, *args, **kwargs):
        with self._global_lock:
            if self._stop_event.is_set():
                raise Stopped('Stopped. New tasks no longer available.')

            self._current_task_id += 1
            func, start_event = self._func_wrapper(self._current_task_id, func, *args, **kwargs)
            self._executor.submit(func)

        start_event.wait()

    def shutdown(self):
        with self._global_lock:
            self._executor.shutdown(wait=False)
            self._stop_event.set()

    def join(self):
        self._stop_event.wait()
        self._executor.shutdown(wait=True)

    def next_value(self):
        with self._global_lock:
            if self._stop_event.is_set():
                raise Stopped('Stopped. No more values available.')

            self._orderer.step()
            current = self._orderer.current

        while True:
            if self._stop_event.is_set():
                raise Stopped('Stopped. No more values available.')

            if self._idorder.wait_for_id(current, timeout=1.0):
                retval = self._retvals[current]
                del self._retvals[current]
                return retval
