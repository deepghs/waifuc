from waifuc.action import NoMonochromeAction, AlignMinSizeAction, TaggingAction
from waifuc.source import DanbooruSource

# crawl images from Danbooru
source = DanbooruSource(['surtr_(arknights)'])
source = source.attach(
    AlignMinSizeAction(640),
    # all the images will be tagged!!!!!
    # no matter if it is colorful or not
    TaggingAction(),

    # monochrome images dropped
    # there is NO need to tag them actually
    NoMonochromeAction(),
)
