from waifuc.export import TextualInversionExporter
from waifuc.source import LocalSource

if __name__ == '__main__':
    # Images from your disk
    s = LocalSource('/data/amiya_zerochan')
    s.export(
        TextualInversionExporter('/data/amiya_zerochan_save')
    )
