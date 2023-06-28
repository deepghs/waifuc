import copy
from typing import Iterator

from tqdm.auto import tqdm

from ..action import BaseAction
from ..export import BaseExporter
from ..model import ImageItem


class BaseDataSource:
    def _iter(self) -> Iterator[ImageItem]:
        raise NotImplementedError

    def _iter_from(self) -> Iterator[ImageItem]:
        for item in tqdm(self._iter(), desc=f'{self.__class__.__name__}'):
            yield item

    def __iter__(self) -> Iterator[ImageItem]:
        yield from self._iter_from()

    def attach(self, *actions: BaseAction) -> 'AttachedDataSource':
        return AttachedDataSource(self, *actions)

    def export(self, exporter: BaseExporter):
        exporter = copy.deepcopy(exporter)
        exporter.reset()
        return exporter.export_from(iter(self))


class AttachedDataSource(BaseDataSource):
    def __init__(self, source: BaseDataSource, *actions: BaseAction):
        self.source = source
        self.actions = actions

    def _iter(self) -> Iterator[ImageItem]:
        t = self.source
        for action in self.actions:
            action = copy.deepcopy(action)
            action.reset()
            t = action.iter_from(t)

        yield from t

    def _iter_from(self) -> Iterator[ImageItem]:
        yield from self._iter()
