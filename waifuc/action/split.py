from typing import Iterator

from imgutils.detect import detect_person

from .base import BaseAction
from ..model import ImageItem


class PersonSplitAction(BaseAction):
    def __init__(self, level: str = 'm', version: str = 'v1.1',
                 conf_threshold: float = 0.3, iou_threshold: float = 0.5):
        self.level = level
        self.version = version
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        detection = detect_person(item.image, self.level, self.version,
                                  conf_threshold=self.conf_threshold, iou_threshold=self.iou_threshold)
        for area, _, _ in detection:
            yield ImageItem(item.image.crop(area), item.meta)

    def reset(self):
        pass
