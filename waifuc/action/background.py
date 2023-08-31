from imgutils.segment import segment_rgba_with_isnetis

from .base import ProcessAction
from ..model import ImageItem


class BackgroundRemovalAction(ProcessAction):
    def process(self, item: ImageItem) -> ImageItem:
        _, image = segment_rgba_with_isnetis(item.image)
        return ImageItem(image, item.meta)
