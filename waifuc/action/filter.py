from imgutils.validate import is_monochrome

from .base import FilterAction
from ..model import ImageItem


class NoMonochromeAction(FilterAction):
    def check(self, item: ImageItem) -> bool:
        return not is_monochrome(item.image)


class OnlyMonochromeAction(FilterAction):
    def check(self, item: ImageItem) -> bool:
        return is_monochrome(item.image)
