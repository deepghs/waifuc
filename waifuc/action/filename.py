from typing import Iterator

from .base import BaseAction
from ..model import ImageItem


class FileExtAction(BaseAction):
    def __init__(self, ext: str):
        self.ext = ext
        self.untitles = 0

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if 'filename' in item.meta:
            filebody, _ = item.meta['filename']
            filename = f'{filebody}{self.ext}'
        else:
            self.untitles += 1
            filename = f'untitled_{self.untitles}{self.ext}'

        yield ImageItem(item.image, {**item.meta, 'filename': filename})

    def reset(self):
        self.untitles = 0
