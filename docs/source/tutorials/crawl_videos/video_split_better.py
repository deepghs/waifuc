from waifuc.action import PersonSplitAction, FilterSimilarAction, FileOrderAction, MinSizeFilterAction, FaceCountAction
from waifuc.export import SaveExporter
from waifuc.source import VideoSource

if __name__ == '__main__':
    source = VideoSource.from_directory('/data/videos')
    source = source.attach(
        # filter similar on full frames (e.g. OPs, EDs)
        FilterSimilarAction(),

        # split for each person
        PersonSplitAction(),

        # must contain only 1 face
        FaceCountAction(1),

        # filter images with min(width, height) < 320
        MinSizeFilterAction(320),

        # filter similar person images
        FilterSimilarAction(),

        # rename the files in order with png format
        FileOrderAction(ext='.png'),
    )
    source.export(
        SaveExporter('/data/dstdataset')
    )
