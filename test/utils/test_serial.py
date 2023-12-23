import random
import time
from threading import Event, Thread

import pytest

from waifuc.utils import SerializableParallelModule, Stopped, NonSerializableParallelModule


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
def serial_send_20(serial):
    event = Event()

    def _t():
        for i in range(20):
            try:
                serial.submit_task(_calc_fn, i)
            except Stopped:
                break

        event.set()
        time.sleep(1.0)
        serial.shutdown()
        serial.join()

    thread = Thread(target=_t)
    thread.start()

    try:
        yield thread, event
    finally:
        thread.join()


@pytest.fixture()
def serial_sending_thread(serial_send_20):
    thread, _ = serial_send_20
    yield thread


@pytest.fixture()
def serial_send_end_event(serial_send_20):
    _, event = serial_send_20
    yield event


@pytest.fixture()
def non_serial():
    s = NonSerializableParallelModule(max_workers=4)
    try:
        yield s
    finally:
        s.join()


@pytest.fixture()
def non_serial_send_20(non_serial):
    event = Event()

    def _t():
        for i in range(20):
            try:
                non_serial.submit_task(_calc_fn, i)
            except Stopped:
                break

        event.set()
        time.sleep(1.0)
        non_serial.shutdown()
        non_serial.join()

    thread = Thread(target=_t)
    thread.start()

    try:
        yield thread, event
    finally:
        thread.join()


@pytest.fixture()
def non_serial_sending_thread(non_serial_send_20):
    thread, _ = non_serial_send_20
    yield thread


@pytest.fixture()
def non_serial_send_end_event(non_serial_send_20):
    _, event = non_serial_send_20
    yield event


@pytest.mark.unittest
class TestUtilsSerial:
    @pytest.mark.parametrize(['try_cnt'], [(i_,) for i_ in range(1, 6)])
    @pytest.mark.parametrize(['max_read'], [(10,), (15,), (None,)])
    def test_run_serial(self, serial, serial_sending_thread, serial_send_end_event, max_read, try_cnt):
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

    @pytest.mark.parametrize(['try_cnt'], [(i_,) for i_ in range(1, 6)])
    @pytest.mark.parametrize(['max_read'], [(10,), (15,), (None,)])
    def test_run_non_serial(self, non_serial, non_serial_sending_thread, non_serial_send_end_event, max_read, try_cnt):
        time.sleep(1 + random.random() * 0.5)
        retvals = []
        if max_read is None:
            max_read = 1 << 31

        i = 0
        while i < max_read:
            try:
                v = non_serial.next_value()
            except Stopped:
                break
            else:
                retvals.append(v)
            i += 1

        non_serial.shutdown()
        max_read = min(20, max_read)
        retvals = sorted(retvals)
        assert len(retvals) == max_read
