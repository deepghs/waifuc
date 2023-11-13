from waifuc.export import SaveExporter
from waifuc.source import LocalSource

if __name__ == '__main__':
    source = LocalSource('/data/mydataset')
    # WRONG USAGE!!!!! no variable for caching the processed source
    source.attach(
        XXXAction()
    )

    # these images will NOT! NOT! NOT! be processed by XXXAction
    source.export(SaveExporter('/data/dstdataset'))
