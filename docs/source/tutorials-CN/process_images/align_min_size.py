from waifuc.action import AlignMinSizeAction
from waifuc.export import SaveExporter
from waifuc.source import LocalSource

if __name__ == '__main__':
    source = LocalSource('/data/raw')
    source = source.attach(
        AlignMinSizeAction(800),
    )

    source.export(SaveExporter('/data/dstdataset'))
