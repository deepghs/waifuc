import random
import time
from threading import Event, Thread

import pytest

from waifuc.utils import SerializableParallelModule, Stopped


def _calc_fn(x):
    time.sleep(random.random() * 0.5)
    return x ** 2


@pytest.fixture()
def serial():
    s = SerializableParallelModule(max_workers=4)
    try:
        yield s
    finally:
        s.join()


@pytest.fixture()
def send_20_nums(serial):
    event = Event()

    def _t():
        for i in range(20):
            try:
                serial.submit_task(_calc_fn, i)
            except Stopped:
                break

        event.set()
        time.sleep(0.5)
        serial.shutdown()
        serial.join()

    thread = Thread(target=_t)
    thread.start()

    try:
        yield thread, event
    finally:
        thread.join()


@pytest.fixture()
def sending_thread(send_20_nums):
    thread, _ = send_20_nums
    yield thread


@pytest.fixture()
def send_end_event(send_20_nums):
    _, event = send_20_nums
    yield event


@pytest.mark.unittest
class TestUtilsSerial:
    @pytest.mark.parametrize(['try_cnt'], [(i_,) for i_ in range(1, 6)])
    @pytest.mark.parametrize(['max_read'], [(10,), (15,), (None,)])
    def test_run_simple(self, serial, sending_thread, send_end_event, max_read, try_cnt):
        time.sleep(1 + random.random() * 0.5)
        retvals = []
        if max_read is None:
            max_read = 1 << 31

        i = 0
        while i < max_read:
            try:
                v = serial.next_value()
            except Stopped:
                break
            else:
                retvals.append(v)
            i += 1

        serial.shutdown()
        assert retvals == [i ** 2 for i in range(min(20, max_read))]
