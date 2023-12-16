from threading import Lock, Event
from typing import Dict, Optional


class Orderer:
    def step(self) -> int:
        raise NotImplementedError

    def wait_for_num(self, num: int, timeout: Optional[float] = None) -> bool:
        raise NotImplementedError


class NoBlockOrderer(Orderer):
    def __init__(self):
        self._current = -1

    def step(self) -> int:
        self._current += 1
        return self._current

    def wait_for_num(self, num: int, timeout: Optional[float] = None) -> bool:
        return True


class SerializableOrderer(Orderer):
    def __init__(self):
        self._events: Dict[int, Event] = {}
        self._current = -1
        self._lock = Lock()

    def step(self) -> int:
        with self._lock:
            self._current += 1
            if self._current in self._events:
                self._events[self._current].set()
                del self._events[self._current]

            return self._current

    def wait_for_num(self, num: int, timeout: Optional[float] = None) -> bool:
        if num < 0:
            raise ValueError(f'Unsupported number {num!r}!')
        with self._lock:
            if num <= self._current:
                return True

            if num not in self._events:
                event = Event()
                self._events[num] = event
            else:
                event = self._events[num]

        return event.wait(timeout=timeout)
