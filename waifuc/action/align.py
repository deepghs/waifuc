import math
from typing import Tuple

from PIL import Image
from imgutils.data import load_image

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


class AlignMaxAreaAction(ProcessAction):
    def __init__(self, size: int):
        self.size = size

    def process(self, item: ImageItem) -> ImageItem:
        image = item.image
        if self.size ** 2 < image.height * image.width:
            r = ((image.height * image.width) / (self.size ** 2)) ** 0.5
            new_width = int(math.ceil(image.width / r))
            new_height = int(math.ceil(image.height / r))
            image = image.resize((new_width, new_height))

        return ImageItem(image, item.meta)


class PaddingAlignAction(ProcessAction):
    def __init__(self, size: Tuple[int, int], color: str = 'white'):
        self.width, self.height = size
        self.color = color

    def process(self, item: ImageItem) -> ImageItem:
        image = load_image(item.image, force_background=None, mode='RGBA')
        r = min(self.width / image.width, self.height / image.height)
        resized = image.resize((int(image.width * r), int(image.height * r)))

        new_image = Image.new('RGBA', (self.width, self.height), self.color)
        left, top = int((new_image.width - resized.width) // 2), int((new_image.height - resized.height) // 2)
        new_image.paste(resized, (left, top, left + resized.width, top + resized.height), resized)
        return ImageItem(new_image.convert(item.image.mode), item.meta)
