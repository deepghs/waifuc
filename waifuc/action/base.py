from typing import Iterator, List

from ..model import ImageItem


class BaseAction:
    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        raise NotImplementedError

    def __rshift__(self, other):
        if not isinstance(self, ComposedAction):
            if not isinstance(other, ComposedAction):
                return ComposedAction(self, other)
            else:
                return ComposedAction(self, *other._actions)
        else:
            if not isinstance(other, ComposedAction):
                return ComposedAction(*self._actions, other)
            else:
                return ComposedAction(*self._actions, *other._actions)


class ProcessAction(BaseAction):
    def process(self, item: ImageItem) -> ImageItem:
        raise NotImplementedError

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        yield self.process(item)

    def __call__(self, item: ImageItem) -> ImageItem:
        return self.process(item)


class FilterAction(BaseAction):
    def check(self, item: ImageItem) -> bool:
        raise NotImplementedError

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if self.check(item):
            yield item

    def __call__(self, item: ImageItem) -> bool:
        return self.check(item)


class ComposedAction(BaseAction):
    def __init__(self, *actions: BaseAction):
        self._actions: List[BaseAction] = list(actions)

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        def _layer(_layer_id):
            if _layer_id == 0:
                yield from self._actions[_layer_id].iter(item)
            else:
                for img_item in _layer(_layer_id - 1):
                    yield from self._actions[_layer_id].iter(img_item)

        yield from _layer(len(self._actions) - 1)
