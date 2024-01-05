from typing import Optional, Mapping, Any

from imgutils.restore import remove_adversarial_noise
from imgutils.validate import safe_check

from .base import ProcessAction
from ..model import ImageItem


class SafetyAction(ProcessAction):
    def __init__(self, cfg_adversarial: Optional[Mapping[str, Any]] = None,
                 cfg_safe_check: Optional[Mapping[str, Any]] = None):
        self.cfg_adversarial = dict(cfg_adversarial or {})
        self.cfg_safe_check = dict(cfg_safe_check or {})

    def process(self, item: ImageItem) -> ImageItem:
        image = item.image
        safe_tag, _ = safe_check(image, **self.cfg_safe_check)
        if safe_tag != 'safe':
            image = remove_adversarial_noise(image, **self.cfg_adversarial)

        return ImageItem(image, item.meta)
