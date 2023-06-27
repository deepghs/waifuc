from typing import Optional

from imgutils.data import load_image

from .base import ProcessAction
from ..model import ImageItem


class ModeConvertAction(ProcessAction):
    def __init__(self, mode='RGB', force_background: Optional[str] = 'white'):
        self.mode = mode
        self.force_background = force_background

    def process(self, item: ImageItem) -> ImageItem:
        image = load_image(item.image, mode=self.mode, force_background=self.force_background)
        return ImageItem(image, item.meta)
