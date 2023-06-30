import random
from typing import Iterator, Optional

from .base import BaseDataSource
from ..model import ImageItem


class ComposedDataSource(BaseDataSource):
    def __init__(self, *sources: BaseDataSource):
        self.sources = sources

    def _iter(self) -> Iterator[ImageItem]:
        for source in self.sources:
            yield from iter(source)

    def _iter_from(self) -> Iterator[ImageItem]:
        yield from self._iter()


class ParallelDataSource(BaseDataSource):
    def __init__(self, *sources: BaseDataSource, seed: Optional[int] = None):
        self.sources = sources
        self.random = random.Random(seed)

    def _iter(self) -> Iterator[ImageItem]:
        iters = [iter(source) for source in self.sources]
        while len(iters) > 0:
            id_ = self.random.choice(range(len(iters)))
            iter_ = iters[id_]

            try:
                yield next(iter_)
            except StopIteration:
                iters.pop(id_)

    def _iter_from(self) -> Iterator[ImageItem]:
        yield from self._iter()
