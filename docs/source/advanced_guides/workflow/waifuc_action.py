from waifuc.action import NoMonochromeAction, AlignMinSizeAction, TaggingAction
from waifuc.source import DanbooruSource

# crawl Surtr's sexy images from Danbooru
source = DanbooruSource(['surtr_(arknights)'])

# 1. Drop the monochrome images.
# 2. If the image is too large, resize it to a smaller size.
# 3. Tag the images.
source = source.attach(
    NoMonochromeAction(),
    AlignMinSizeAction(640),
    TaggingAction()
)
