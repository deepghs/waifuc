from waifuc.action import ClassFilterAction
from waifuc.export import SaveExporter
from waifuc.source import LocalSource

if __name__ == '__main__':
    source = LocalSource('/data/raw')
    # only keep the illustrations and bangumi screenshots
    source = source.attach(
        ClassFilterAction(['illustration', 'bangumi']),
    )

    source.export(SaveExporter('/data/dstdataset'))
