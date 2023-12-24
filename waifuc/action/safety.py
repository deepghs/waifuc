from imgutils.restore import remove_adversarial_noise

from .base import ProcessAction
from ..model import ImageItem


class SafetyAction(ProcessAction):
    def process(self, item: ImageItem) -> ImageItem:
        return ImageItem(remove_adversarial_noise(item.image), item.meta)
