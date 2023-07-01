import os
from typing import Iterator, Optional

from .base import BaseAction
from ..model import ImageItem


class FileExtAction(BaseAction):
    def __init__(self, ext: str):
        self.ext = ext
        self.untitles = 0

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if 'filename' in item.meta:
            filebody, _ = os.path.splitext(item.meta['filename'])
            filename = f'{filebody}{self.ext}'
        else:
            self.untitles += 1
            filename = f'untitled_{self.untitles}{self.ext}'

        yield ImageItem(item.image, {**item.meta, 'filename': filename})

    def reset(self):
        self.untitles = 0


class FileOrderAction(BaseAction):
    def __init__(self, ext: Optional[str] = '.png'):
        self.ext = ext
        self._current = 0

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        self._current += 1
        if 'filename' in item.meta:
            _, ext = os.path.splitext(item.meta['filename'])
            new_filename = f'{self._current}{self.ext or ext}'
        else:
            if not self.ext:
                raise ValueError('No extension name provided for unnamed file.')
            else:
                new_filename = f'{self._current}{self.ext}'

        yield ImageItem(item.image, {**item.meta, 'filename': new_filename})

    def reset(self):
        self._current = 0
