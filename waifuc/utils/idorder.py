from threading import Lock, Event
from typing import Set, Dict, Optional


class IDOrder:
    def __init__(self):
        self._events: Dict[int, Event] = {}
        self._exist_ids: Set[int] = set()
        self._global_lock = Lock()

    def set_id(self, id_: int):
        with self._global_lock:
            if id_ not in self._exist_ids:
                self._exist_ids.add(id_)
                if id_ in self._events:
                    self._events[id_].set()
                    del self._events[id_]

    def _prepare_for_id(self, id_: int):
        if id_ in self._exist_ids:
            return None

        if id_ not in self._events:
            event = Event()
            self._events[id_] = event
        else:
            event = self._events[id_]

        return event

    def wait_for_id(self, id_: int, timeout: Optional[float] = None) -> bool:
        with self._global_lock:
            event = self._prepare_for_id(id_)
            if event is None:
                return True

        return event.wait(timeout=timeout)

    def is_set_id(self, id_: int) -> bool:
        with self._global_lock:
            event = self._prepare_for_id(id_)
            return True if event is None else event.is_set()
