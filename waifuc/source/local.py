import os
import re
from typing import Iterator

from PIL import UnidentifiedImageError

from .base import RootDataSource
from ..model import ImageItem


class LocalSource(RootDataSource):
    def __init__(self, directory: str, recursive: bool = True):
        self.directory = directory
        self.recursive = recursive

    def _iter_files(self):
        if self.recursive:
            for directory, _, files in os.walk(self.directory):
                group_name = re.sub(r'[\W_]+', '_', directory).strip('_')
                for file in files:
                    yield os.path.join(directory, file), group_name
        else:
            group_name = re.sub(r'[\W_]+', '_', self.directory).strip('_')
            for file in os.listdir(self.directory):
                yield os.path.join(self.directory, file), group_name

    def _iter(self) -> Iterator[ImageItem]:
        for file, group_name in self._iter_files():
            try:
                origin_item = ImageItem.load_from_image(file)
                origin_item.image.load()
            except UnidentifiedImageError:
                continue

            meta = origin_item.meta or {
                'path': os.path.abspath(file),
                'group_id': group_name,
                'filename': os.path.basename(file),
            }
            yield ImageItem(origin_item.image, meta)
