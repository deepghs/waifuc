import copy
from typing import Iterator

from ..action import BaseAction
from ..model import ImageItem


class BaseDataSource:
    def _iter(self) -> Iterator[ImageItem]:
        raise NotImplementedError

    def __iter__(self):
        yield from self._iter()

    def attach(self, *actions: BaseAction):
        actions = [copy.deepcopy(action) for action in actions]
        for action in actions:
            action.reset()
        return AttachedDataSource(self, *actions)


class AttachedDataSource(BaseDataSource):
    def __init__(self, source: BaseDataSource, *actions: BaseAction):
        self.source = source
        self.actions = actions

    def _iter(self) -> Iterator[ImageItem]:
        t = self.source
        for action in self.actions:
            t = action.iter_from(t)

        yield from t
