from functools import partial

from imgutils.tagging import get_deepdanbooru_tags, get_wd14_tags, get_mldanbooru_tags

from .base import BaseAction
from ..model import ImageItem

try:
    from typing import Literal, Iterator
except (ImportError, ModuleNotFoundError):
    from typing_extensions import Literal

_TAGGING_METHODS = {
    'deepdanbooru': get_deepdanbooru_tags,
    'wd14_vit': partial(get_wd14_tags, model_name='ViT'),
    'wd14_convnext': partial(get_wd14_tags, model_name='ConvNext'),
    'wd14_convnextv2': partial(get_wd14_tags, model_name='ConvNextV2'),
    'wd14_swinv2': partial(get_wd14_tags, model_name='SwinV2'),
    'mldanbooru': get_mldanbooru_tags,
}

TaggingMethodTyping = Literal[
    'deepdanbooru', 'wd14_vit', 'wd14_convnext', 'wd14_convnextv2', 'wd14_swinv2', 'mldanbooru']


class TaggingAction(BaseAction):
    def __init__(self, method: TaggingMethodTyping = 'wd14_convnextv2', force: bool = False, **kwargs):
        self.method = _TAGGING_METHODS[method]
        self.force = force
        self.kwargs = kwargs

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if 'tags' in item.meta and not self.force:
            yield item
        else:
            tags = self.method(image=item.image, **self.kwargs)
            yield ImageItem(item.image, {**item.meta, 'tags': tags})
