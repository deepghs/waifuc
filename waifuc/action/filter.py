from typing import List, Optional

from imgutils.detect import detect_faces, detect_heads
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


class FaceCountAction(FilterAction):
    def __init__(self, count: int, level: str = 's', version: str = 'v1.4',
                 conf_threshold: float = 0.25, iou_threshold: float = 0.7):
        self.count = count
        self.level = level
        self.version = version
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

    def check(self, item: ImageItem) -> bool:
        detection = detect_faces(item.image, self.level, self.version,
                                 conf_threshold=self.conf_threshold, iou_threshold=self.iou_threshold)
        return len(detection) == self.count


class HeadCountAction(FilterAction):
    def __init__(self, count: int, level: str = 's', conf_threshold: float = 0.3, iou_threshold: float = 0.7):
        self.count = count
        self.level = level
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

    def check(self, item: ImageItem) -> bool:
        detection = detect_heads(
            item.image, self.level,
            conf_threshold=self.conf_threshold,
            iou_threshold=self.iou_threshold
        )
        return len(detection) == self.count
