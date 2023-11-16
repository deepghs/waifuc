from waifuc.export import SaveExporter
from waifuc.source import LocalSource

if __name__ == '__main__':
    source = LocalSource('/data/mydataset')
    source = source[:100]

    source.export(SaveExporter('/data/dstdataset'))
