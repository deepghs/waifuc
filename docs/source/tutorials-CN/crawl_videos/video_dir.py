from waifuc.export import SaveExporter
from waifuc.source import VideoSource

if __name__ == '__main__':
    source = VideoSource.from_directory('/data/videos')
    source.export(
        SaveExporter('/data/dstdataset')
    )
