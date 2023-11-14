from waifuc.action import PersonSplitAction
from waifuc.export import SaveExporter
from waifuc.source import VideoSource

if __name__ == '__main__':
    source = VideoSource.from_directory('/data/videos')
    source = source.attach(
        PersonSplitAction(),
    )
    source.export(
        SaveExporter('/data/dstdataset')
    )
