import copy
from typing import Iterator, Optional

from tqdm.auto import tqdm

from ..action import BaseAction
from ..export import BaseExporter
from ..model import ImageItem
from ..utils import task_ctx, get_task_names


class BaseDataSource:
    def _iter(self) -> Iterator[ImageItem]:
        raise NotImplementedError  # pragma: no cover

    def _iter_from(self) -> Iterator[ImageItem]:
        yield from self._iter()

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

    def __getitem__(self, item):
        from ..action import SliceSelectAction
        if isinstance(item, slice):
            return self.attach(SliceSelectAction(item.start, item.stop, item.step))
        else:
            raise TypeError(f'Data source\'s getitem only accept slices, but {item!r} found.')

    def attach(self, *actions: BaseAction) -> 'AttachedDataSource':
        return AttachedDataSource(self, *actions)

    def export(self, exporter: BaseExporter, name: Optional[str] = None):
        exporter = copy.deepcopy(exporter)
        exporter.reset()
        with task_ctx(name):
            return exporter.export_from(iter(self))


class NamedDataSource(BaseDataSource):
    def _args(self):
        return None

    def __str__(self):
        return f'{self.__class__.__name__}({", ".join(map(repr, self._args() or []))})'

    def __repr__(self):
        return f'<{self.__class__.__name__} {", ".join(map(repr, self._args() or []))}>'

    def _iter(self) -> Iterator[ImageItem]:
        raise NotImplementedError  # pragma: no cover

    def _iter_from(self) -> Iterator[ImageItem]:
        names = get_task_names()
        if names:
            desc = f'{self} - {".".join(names)}'
        else:
            desc = f'{self}'
        for item in tqdm(self._iter(), desc=desc):
            yield item


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


class EmptySource(BaseDataSource):
    def _iter(self) -> Iterator[ImageItem]:
        yield from []
