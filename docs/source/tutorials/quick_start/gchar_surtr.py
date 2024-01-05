from waifuc.action import NoMonochromeAction, FilterSimilarAction, \
    PersonSplitAction, TaggingAction, FaceCountAction, FirstNSelectAction, \
    CCIPAction, ModeConvertAction, ClassFilterAction, RandomFilenameAction, AlignMinSizeAction
from waifuc.export import TextualInversionExporter
from waifuc.source import GcharAutoSource

if __name__ == '__main__':
    # data source for surtr in arknights, images from many sites will be crawled
    # all supported games and sites can be found at
    # https://narugo1992.github.io/gchar/main/best_practice/supported/index.html#supported-games-and-sites
    # ATTENTION: GcharAutoSource required `git+https://github.com/deepghs/waifuc.git@main#egg=waifuc[gchar]`
    s = GcharAutoSource('surtr')

    # crawl images, process them, and then save them to a directory with given format
    s.attach(
        # preprocess images with white background RGB
        ModeConvertAction('RGB', 'white'),

        # pre-filtering for images
        NoMonochromeAction(),  # no monochrome, greyscale or sketch
        ClassFilterAction(['illustration', 'bangumi']),  # no comic or 3d images
        FilterSimilarAction('all'),  # filter duplicated images

        # human processing
        FaceCountAction(1),  # drop images with 0 or >1 faces
        PersonSplitAction(),  # crop for each person
        FaceCountAction(1),

        # CCIP, filter the character you may not want to see in dataset
        CCIPAction(),

        # if min(height, weight) > 800, resize it to 800
        AlignMinSizeAction(800),

        # tagging with wd14 v2, if you don't need character tag, set character_threshold=1.01
        TaggingAction(force=True),

        FilterSimilarAction('all'),  # filter again
        FirstNSelectAction(200),  # when the 200th images reach this step, stop this pipeline
        RandomFilenameAction(ext='.png'),  # random rename files
    ).export(
        # save to /data/surtr_dataset directory
        # you can change it to your own directory
        TextualInversionExporter('/data/surtr_dataset')
    )
