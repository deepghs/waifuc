from waifuc.action import FaceCountAction
from waifuc.export import SaveExporter
from waifuc.source import LocalSource

if __name__ == '__main__':
    source = LocalSource('/data/raw')
    source = source.attach(
        FaceCountAction(1),
    )

    source.export(SaveExporter('/data/dstdataset'))
