from waifuc.action import NoMonochromeAction
from waifuc.export import SaveExporter
from waifuc.source import LocalSource

if __name__ == '__main__':
    source = LocalSource('/data/raw')
    source = source.attach(
        NoMonochromeAction(),
    )

    source.export(SaveExporter('/data/dstdataset'))
