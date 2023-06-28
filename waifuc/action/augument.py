import os.path
import random
from typing import Iterator, Optional

from hbutils.random import random_sha1

from .base import BaseAction
from ..model import ImageItem


class BaseRandomAction(BaseAction):
    def __init__(self, seed=None):
        self.seed = seed
        self.random = random.Random(self.seed)

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        raise NotImplementedError

    def reset(self):
        self.random = random.Random(self.seed)


class RandomChoiceAction(BaseRandomAction):
    def __init__(self, p=0.5, seed=None):
        BaseRandomAction.__init__(self, seed)
        self.p = p

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if self.random.random() <= self.p:
            yield item


class RandomFilenameAction(BaseRandomAction):
    def __init__(self, ext: Optional[str] = '.png', seed=None):
        BaseRandomAction.__init__(self, seed)
        self.ext = ext

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if 'filename' in item.meta:
            ext = self.ext or os.path.splitext(os.path.basename(item.meta['filename']))[0]
        else:
            if self.ext:
                ext = self.ext
            else:
                raise NameError(f'Extension (ext) must be specified '
                                f'when filename not in metadata of image item - {item!r}.')

        filename = random_sha1(rnd=self.random) + ext
        yield ImageItem(item.image, {**item.meta, 'filename': filename})
