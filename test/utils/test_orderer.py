import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Event
from typing import Optional

import pytest

from waifuc.utils import NoBlockOrderer, SerializableOrderer


@pytest.fixture()
def no_block():
    yield NoBlockOrderer()


@pytest.fixture()
def serializable():
    yield SerializableOrderer()


@pytest.fixture()
def thread_pool():
    tp = ThreadPoolExecutor(max_workers=36)
    try:
        yield tp
    finally:
        tp.shutdown(wait=True)


class ValueEvent:
    def __init__(self):
        self._event = Event()
        self._value = None
        self._lock = Lock()

    def put_value(self, value):
        with self._lock:
            self._event.set()
            self._value = value

    def wait(self, timeout: Optional[float] = None):
        return self._event.wait(timeout=timeout)

    @property
    def is_set(self):
        with self._lock:
            return self._event.is_set()

    @property
    def value(self):
        with self._lock:
            return self._value


@pytest.mark.unittest
class TestUtilsOrderer:

    def test_no_block_orderer(self, no_block):
        assert no_block.current == -1
        assert no_block.wait_for_num(100)
        assert no_block.step() == 0
        assert no_block.wait_for_num(0)
        assert no_block.wait_for_num(100)
        assert no_block.step() == 1
        assert no_block.wait_for_num(0)
        assert no_block.wait_for_num(100)

    @pytest.mark.parametrize(['try_cnt'], [(i_,) for i_ in range(1, 11)])
    def test_serializable(self, serializable, thread_pool, try_cnt):
        assert serializable.current == -1

        def _get_wait_event(num):
            _value = ValueEvent()

            def _call():
                value = serializable.wait_for_num(num)
                _value.put_value(value)

            thread_pool.submit(_call)
            return _value

        with pytest.raises(ValueError):
            serializable.wait_for_num(-100)

        v0 = _get_wait_event(0)
        assert not v0.is_set
        time.sleep(0.5)
        assert not v0.is_set

        assert serializable.step() == 0
        assert v0.wait()
        assert v0.is_set

        v1, v2, v10 = _get_wait_event(1), _get_wait_event(2), _get_wait_event(10)
        assert serializable.step() == 1
        assert v1.wait()
        assert v1.is_set
        assert serializable.wait_for_num(0)

        assert not v2.wait(0.5)
        assert serializable.step() == 2
        assert v2.wait()
        assert v2.is_set

        assert not v10.wait(0.5)
        v10x = _get_wait_event(10)
        assert not v10x.wait(0.5)
        assert [serializable.step() for i in range(10)] == [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        assert v10.wait()
        assert v10.is_set
        assert v10x.is_set
