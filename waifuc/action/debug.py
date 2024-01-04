from typing import Optional, List, Any, Iterator

from .base import ProgressBarAction
from ..model import ImageItem


class ArrivalAction(ProgressBarAction):
    def __init__(self, name: str, total: Optional[int] = None):
        ProgressBarAction.__init__(self, total)
        self.name = name

    def _args(self) -> Optional[List[Any]]:
        return [self.name]

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        yield item

    def reset(self):
        pass
