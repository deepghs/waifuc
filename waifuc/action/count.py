import math
from typing import Iterator, Optional, List, Any

from .base import ActionStop, ProgressBarAction
from ..model import ImageItem


class FirstNSelectAction(ProgressBarAction):
    def __init__(self, n: int):
        ProgressBarAction.__init__(self, n)
        self._n = n
        self._passed = 0

    def _args(self) -> Optional[List[Any]]:
        return [self._n]

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if self._passed < self._n:
            yield item
            self._passed += 1
        else:
            raise ActionStop

    def reset(self):
        self._passed = 0


def _slice_process(start, stop, step):
    start = 0 if start is None else start
    step = 1 if step is None else step
    if not isinstance(start, int) or start < 0:
        raise ValueError(f'Start should be an integer no less than 0, but {start!r} found.')
    if stop is not None and (not isinstance(stop, int) or stop < 0):
        raise ValueError(f'Stop should be an integer no less than 0, but {stop!r} found.')
    if not isinstance(step, int) or step < 1:
        raise ValueError(f'Step should be an integer no less than 1, but {step!r} found.')

    return start, stop, step


class SliceSelectAction(ProgressBarAction):
    def __init__(self, *args):
        if len(args) == 0:
            slice_args = _slice_process(None, None, None)
        elif len(args) == 1:
            slice_args = _slice_process(None, args[0], None)
        elif len(args) == 2:
            slice_args = _slice_process(args[0], args[1], None)
        elif len(args) == 3:
            slice_args = _slice_process(args[0], args[1], args[2])
        else:
            raise ValueError(f'Arguments of {self.__class__.__name__} should no no more than 3, but {args!r} found.')

        self._start, self._stop, self._step = slice_args
        if self._stop is not None:
            self._max = self._start + ((self._stop - self._start - 1) // self._step) * self._step
        else:
            self._max = None
        self._current = 0

        ProgressBarAction.__init__(self, self._count())

    def _args(self) -> Optional[List[Any]]:
        return [self._start, self._stop if self._stop is not None else math.inf, self._step]

    def _count(self):
        if self._stop is None:
            return None
        elif self._step <= self._start:
            return 0
        else:
            return (self._stop - self._start - 1) // self._step + 1

    def _check_current(self):
        if self._stop is not None and self._current >= self._stop:
            return False
        if self._current < self._start:
            return False
        return (self._current - self._start) % self._step == 0

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if self._current > self._max:
            raise ActionStop
        else:
            if self._check_current():
                yield item
            self._current += 1

    def reset(self):
        self._current = 0
