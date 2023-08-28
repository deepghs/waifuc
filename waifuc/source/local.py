import glob
import os
import pathlib
import random
import re
from typing import Iterator

from PIL import UnidentifiedImageError
from imgutils.data import load_image

from .base import RootDataSource
from ..model import ImageItem


class LocalSource(RootDataSource):
    def __init__(self, directory: str, recursive: bool = True, shuffle: bool = False):
        self.directory = directory
        self.recursive = recursive
        self.shuffle = shuffle

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

    def _actual_iter_files(self):
        lst = list(self._iter_files())
        if self.shuffle:
            random.shuffle(lst)
        yield from lst

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


class LocalTISource(RootDataSource):
    def __init__(self, directory: str):
        self.directory = directory

    def _iter(self) -> Iterator[ImageItem]:
        group_name = re.sub(r'[\W_]+', '_', self.directory).strip('_')
        for f in glob.glob(os.path.join(self.directory, '*')):
            if not os.path.isfile(f):
                continue

            try:
                image = load_image(f)
            except UnidentifiedImageError:
                continue

            id_ = os.path.splitext(os.path.basename(f))[0]
            txt_file = os.path.join(self.directory, f'{id_}.txt')
            if os.path.exists(txt_file):
                full_text = pathlib.Path(txt_file).read_text(encoding='utf-8')
                words = re.split(r'\s*,\s*', full_text)
                tags = {word: 1.0 for word in words}
            else:
                tags = {}

            meta = {
                'path': os.path.abspath(f),
                'group_id': group_name,
                'filename': os.path.basename(f),
                'tags': tags,
            }
            yield ImageItem(image, meta)
