from waifuc.export import SaveExporter
from waifuc.source import VideoSource

if __name__ == '__main__':
    source = VideoSource(
        '/data/videos/[IrizaRaws] Oresuki - 03 (BDRip 1920x1080 x264 10bit FLAC).mkv'
    )
    source.export(
        SaveExporter('/data/dstdataset')
    )
