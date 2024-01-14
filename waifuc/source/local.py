import os
import pathlib
import random
import re
import warnings
from typing import Iterator, Optional, List, Any

from PIL import UnidentifiedImageError
from imgutils.data import load_image
from tqdm.auto import tqdm

from .base import NamedDataSource
from .frames import _FrameSource
from ..model import ImageItem


class BaseDirectorySource(NamedDataSource):
    def __init__(self, directory: str, recursive: bool = True, shuffle: bool = False):
        self.directory = directory
        self.recursive = recursive
        self.shuffle = shuffle

    def _args(self) -> Optional[List[Any]]:
        return [self.directory]

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
        yield from tqdm(lst, desc=f'Loading from {self.directory!r}')

    def _iter(self) -> Iterator[ImageItem]:
        raise NotImplementedError  # pragma: no cover


class LocalSource(BaseDirectorySource):
    def __init__(self, directory: str, recursive: bool = True, shuffle: bool = False):
        BaseDirectorySource.__init__(self, directory, recursive, shuffle)

    def _iter(self) -> Iterator[ImageItem]:
        for file, group_name in self._actual_iter_files():
            try:
                origin_item = ImageItem.load_from_image(file)
                origin_item.image.load()
            except UnidentifiedImageError:
                continue
            except OSError:
                warnings.warn(f'File {file} is truncated or corrupted, skipped.')
                continue

            target_filename = os.path.basename(file)
            meta = origin_item.meta or {
                'path': os.path.abspath(file),
                'group_id': group_name,
                'filename': target_filename,
            }
            yield from _FrameSource(origin_item.image, meta)


class LocalTISource(BaseDirectorySource):
    def __init__(self, directory: str, recursive: bool = True, shuffle: bool = False):
        BaseDirectorySource.__init__(self, directory, recursive, shuffle)

    def _iter(self) -> Iterator[ImageItem]:
        for file, group_name in self._actual_iter_files():
            try:
                image = load_image(file)
            except UnidentifiedImageError:
                continue
            except OSError:
                warnings.warn(f'File {file} is truncated or corrupted, skipped.')
                continue

            filename_body = os.path.splitext(os.path.basename(file))[0]
            txt_file = os.path.join(self.directory, f'{filename_body}.txt')
            if os.path.exists(txt_file):
                full_text = pathlib.Path(txt_file).read_text(encoding='utf-8')
                words = re.split(r'\s*,\s*', full_text)
                tags = {word: 1.0 for word in words}
            else:
                tags = {}

            meta = {
                'path': os.path.abspath(file),
                'group_id': group_name,
                'filename': os.path.basename(file),
                'tags': tags,
            }
            yield ImageItem(image, meta)
