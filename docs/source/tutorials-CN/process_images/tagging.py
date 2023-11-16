from waifuc.action import TaggingAction
from waifuc.export import TextualInversionExporter
from waifuc.source import LocalSource

if __name__ == '__main__':
    source = LocalSource('/data/raw')
    source = source.attach(
        TaggingAction(),
    )

    source.export(TextualInversionExporter('/data/dstdataset'))
