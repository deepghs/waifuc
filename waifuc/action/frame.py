import os
from typing import Iterator

from .base import BaseAction
from ..model import ImageItem


class FrameSplitAction(BaseAction):
    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if not hasattr(item.image, 'n_frames') or item.image.n_frames == 1:
            yield item
        else:
            for i in range(item.image.n_frames):
                item.image.seek(i)
                frame_image = item.image.copy()

                if 'filename' not in item.meta:
                    meta_info = {
                        **item.meta,
                        'frame_id': i,
                    }
                else:
                    filename, fileext = os.path.splitext(item.meta['filename'])
                    meta_info = {
                        **item.meta,
                        'filename': f'{filename}_frame_{i}{fileext}',
                        'frame_id': i,
                    }
                yield ImageItem(frame_image, meta_info)

    def reset(self):
        pass
