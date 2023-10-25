from typing import Iterator, Iterable

from ..model import ImageItem


class ActionStop(Exception):
    pass


class BaseAction:
    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        raise NotImplementedError  # pragma: no cover

    def iter_from(self, iter_: Iterable[ImageItem]) -> Iterator[ImageItem]:
        for item in iter_:
            try:
                yield from self.iter(item)
            except ActionStop:
                break

    def reset(self):
        raise NotImplementedError  # pragma: no cover


class ProcessAction(BaseAction):
    def process(self, item: ImageItem) -> ImageItem:
        raise NotImplementedError  # pragma: no cover

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        yield self.process(item)

    def reset(self):
        pass

    def __call__(self, item: ImageItem) -> ImageItem:
        return self.process(item)


class FilterAction(BaseAction):
    def check(self, item: ImageItem) -> bool:
        raise NotImplementedError  # pragma: no cover

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if self.check(item):
            yield item

    def reset(self):
        pass

    def __call__(self, item: ImageItem) -> bool:
        return self.check(item)
