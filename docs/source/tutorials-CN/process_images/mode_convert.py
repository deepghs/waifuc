from waifuc.action import ModeConvertAction
from waifuc.export import SaveExporter
from waifuc.source import LocalSource

if __name__ == '__main__':
    source = LocalSource('/data/mydataset')
    source = source.attach(
        ModeConvertAction(mode='RGB', force_background='white'),
    )

    source.export(SaveExporter('/data/dstdataset'))
