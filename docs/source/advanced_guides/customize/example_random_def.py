import copy
import random
from typing import Iterator

from PIL import ImageOps

from waifuc.action import BaseAction
from waifuc.model import ImageItem


class MyRandomAction(BaseAction):
    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        r = random.random()
        if r < 0.3:
            # just drop this image, no item yielded
            pass
        else:
            # pass the item out
            item.meta['random'] = r  # set meta info
            item.meta['filename'] = f'random_{r:.4f}.png'  # set filename
            yield item

            if r > 0.7:  # pass another mirrored version out
                # copy the item to avoid using the same object
                item = copy.deepcopy(item)
                item.meta['random'] = r  # set meta info
                item.meta['filename'] = f'random_{r:.4f}_inv.png'  # set filename
                item.image = ImageOps.mirror(item.image)
                # yield both original item and mirrored item
                yield item
            else:
                # yield the original item only
                pass

    def reset(self):
        pass
