from waifuc.action import NoMonochromeAction, AlignMinSizeAction, TaggingAction
from waifuc.source import DanbooruSource

# crawl images from danbooru
source = DanbooruSource(['surtr_(arknights)'])
source = source.attach(NoMonochromeAction())  # just drop the monochrome images

# process the colorful images
source = source.attach(
    AlignMinSizeAction(640),
    TaggingAction(),
)
