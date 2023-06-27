from .base import ProcessAction
from ..model import ImageItem


class AlignMaxSizeAction(ProcessAction):
    def __init__(self, max_size: int):
        self._max_size = max_size

    def process(self, item: ImageItem) -> ImageItem:
        image = item.image
        ms = max(image.width, image.height)
        if ms > self._max_size:
            r = ms / self._max_size
            image = image.resize((int(image.width / r), int(image.height / r)))

        return ImageItem(image, item.meta)


class AlignMinSizeAction(ProcessAction):
    def __init__(self, min_size: int):
        self._min_size = min_size

    def process(self, item: ImageItem) -> ImageItem:
        image = item.image
        ms = min(image.width, image.height)
        if ms > self._min_size:
            r = ms / self._min_size
            image = image.resize((int(image.width / r), int(image.height / r)))

        return ImageItem(image, item.meta)
