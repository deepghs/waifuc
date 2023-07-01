import os
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

        if 'filename' in item.meta:
            filename = item.meta['filename']
            filebody, ext = os.path.splitext(filename)
        else:
            filebody, ext = None, None

        for i, (area, _, _) in enumerate(detection):
            if filebody is not None:
                new_meta = {**item.meta, 'filename': f'{filebody}_person{i}{ext}'}
            else:
                new_meta = item.meta

            yield ImageItem(item.image.crop(area), new_meta)

    def reset(self):
        pass
