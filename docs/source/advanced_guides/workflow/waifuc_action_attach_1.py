from waifuc.action import NoMonochromeAction, AlignMinSizeAction, TaggingAction
from waifuc.source import DanbooruSource

# crawl images from danbooru
source = DanbooruSource(['surtr_(arknights)'])
source = source.attach(
    NoMonochromeAction(),
    AlignMinSizeAction(640),
    TaggingAction(),
)
