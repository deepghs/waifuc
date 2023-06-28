from typing import List, Optional

from imgutils.validate import is_monochrome, anime_classify, anime_rating

from .base import FilterAction
from ..model import ImageItem

try:
    from typing import Literal
except (ImportError, ModuleNotFoundError):
    from typing_extensions import Literal


class NoMonochromeAction(FilterAction):
    def check(self, item: ImageItem) -> bool:
        return not is_monochrome(item.image)


class OnlyMonochromeAction(FilterAction):
    def check(self, item: ImageItem) -> bool:
        return is_monochrome(item.image)


ImageClassTyping = Literal['illustration', 'bangumi', 'comic', '3d']


class ClassFilterAction(FilterAction):
    def __init__(self, classes: List[ImageClassTyping], threshold: Optional[float] = None, **kwargs):
        self.classes = classes
        self.threshold = threshold
        self.kwargs = kwargs

    def check(self, item: ImageItem) -> bool:
        cls, score = anime_classify(item.image, **self.kwargs)
        return cls in self.classes and (self.threshold is None or score >= self.threshold)


ImageRatingTyping = Literal['safe', 'r15', 'r18']


class RatingFilterAction(FilterAction):
    def __init__(self, ratings: List[ImageRatingTyping], threshold: Optional[float] = None, **kwargs):
        self.ratings = ratings
        self.threshold = threshold
        self.kwargs = kwargs

    def check(self, item: ImageItem) -> bool:
        rating, score = anime_rating(item.image, **self.kwargs)
        return rating in self.ratings and (self.threshold is None or score >= self.threshold)
