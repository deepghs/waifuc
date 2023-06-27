from typing import Iterator

from ..model import ImageItem


class BaseDataSource:
    def _iter(self) -> Iterator[ImageItem]:
        raise NotImplementedError

    def __iter__(self):
        yield from self._iter()
