import copy
from typing import Iterator, Optional

from tqdm.auto import tqdm

from ..action import BaseAction
from ..export import BaseExporter
from ..model import ImageItem
from ..utils import task_ctx, get_task_names


class BaseDataSource:
    def _iter(self) -> Iterator[ImageItem]:
        raise NotImplementedError

    def _iter_from(self) -> Iterator[ImageItem]:
        names = get_task_names()
        if names:
            desc = f'{self.__class__.__name__} - {".".join(names)}'
        else:
            desc = f'{self.__class__.__name__}'
        for item in tqdm(self._iter(), desc=desc):
            yield item

    def __iter__(self) -> Iterator[ImageItem]:
        yield from self._iter_from()

    def __or__(self, other):
        from .compose import ParallelDataSource
        if isinstance(self, ParallelDataSource):
            if isinstance(other, ParallelDataSource):
                return ParallelDataSource(*self.sources, *other.sources)
            else:
                return ParallelDataSource(*self.sources, other)
        else:
            if isinstance(other, ParallelDataSource):
                return ParallelDataSource(self, *other.sources)
            else:
                return ParallelDataSource(self, other)

    def __add__(self, other):
        from .compose import ComposedDataSource
        if isinstance(self, ComposedDataSource):
            if isinstance(other, ComposedDataSource):
                return ComposedDataSource(*self.sources, *other.sources)
            else:
                return ComposedDataSource(*self.sources, other)
        else:
            if isinstance(other, ComposedDataSource):
                return ComposedDataSource(self, *other.sources)
            else:
                return ComposedDataSource(self, other)

    def attach(self, *actions: BaseAction) -> 'AttachedDataSource':
        return AttachedDataSource(self, *actions)

    def export(self, exporter: BaseExporter, name: Optional[str] = None):
        exporter = copy.deepcopy(exporter)
        exporter.reset()
        with task_ctx(name):
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
