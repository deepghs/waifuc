import os.path
from typing import Iterator

from PIL import Image

from .base import BaseDataSource
from ..model import ImageItem


class _FrameSource(BaseDataSource):
    def __init__(self, image: Image.Image, meta_info: dict):
        self.image = image
        self.meta_info = dict(meta_info or {})

    def _iter(self) -> Iterator[ImageItem]:
        if self.image.n_frames == 1:
            yield ImageItem(self.image, self.meta_info)
        else:
            for i in range(self.image.n_frames):
                self.image.seek(i)
                frame_image = self.image.copy()

                if 'filename' not in self.meta_info:
                    meta_info = self.meta_info
                else:
                    filename, fileext = os.path.splitext(self.meta_info['filename'])
                    meta_info = {
                        **self.meta_info,
                        'filename': f'{filename}_frame_{i}{fileext}',
                        'frame_id': i,
                    }
                yield ImageItem(frame_image, meta_info)
