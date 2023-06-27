from typing import Iterator

from .base import BaseAction
from ..model import ImageItem


class FirstNSelectAction(BaseAction):
    def __init__(self, n: int):
        self._n = n
        self._passed = 0

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if self._passed < self._n:
            yield item
            self._passed += 1


class SliceSelectAction(BaseAction):
    def __init__(self, *args):
        self._range = range(*args)
        self._current = 0

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if self._current in self._range:
            yield item
            self._current += 1
