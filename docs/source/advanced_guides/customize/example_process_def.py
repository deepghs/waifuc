from imgutils.detect import detect_heads

from waifuc.action import ProcessAction
from waifuc.model import ImageItem


class CutHeadAction(ProcessAction):
    def process(self, item: ImageItem) -> ImageItem:
        area, type_, score = detect_heads(item.image)[0]
        return ImageItem(
            image=item.image.crop(area),
            meta=item.meta,
        )
