from imgutils.validate import anime_classify

from waifuc.action import FilterAction
from waifuc.model import ImageItem


class ComicOnlyAction(FilterAction):
    def check(self, item: ImageItem) -> bool:
        type_, _ = anime_classify(item.image)
        return type_ == 'comic'
