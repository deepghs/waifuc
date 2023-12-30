from imgutils.restore import remove_adversarial_noise

from .base import ProcessAction
from ..model import ImageItem


class SafetyAction(ProcessAction):
    def __init__(self, **cfg_adversarial):
        self.cfg_adversarial = cfg_adversarial

    def process(self, item: ImageItem) -> ImageItem:
        return ImageItem(remove_adversarial_noise(item.image, **self.cfg_adversarial), item.meta)
