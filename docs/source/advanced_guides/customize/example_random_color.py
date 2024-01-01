import random
from typing import Iterator

from PIL import Image

from waifuc.export import SaveExporter
from waifuc.model import ImageItem
from waifuc.source import BaseDataSource


class RandomColorSource(BaseDataSource):
    def __init__(self, min_width: int = 256, max_width: int = 512,
                 min_height: int = 256, max_height: int = 512):
        self.min_width, self.max_width = min_width, max_width
        self.min_height, self.max_height = min_height, max_height

    def _iter(self) -> Iterator[ImageItem]:
        # endlessly create random images
        while True:
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            width = random.randint(self.min_width, self.max_width)
            height = random.randint(self.min_height, self.max_height)

            image = Image.new('RGB', (width, height), (r, g, b))
            yield ImageItem(
                image=image,
                meta={
                    'color': {'r': r, 'g': g, 'b': b},
                    'size': {'width': width, 'height': height},
                }
            )


if __name__ == '__main__':
    s = RandomColorSource()
    # only 30 images are needed
    s[:30].export(SaveExporter('test_random_color'))
