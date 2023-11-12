from waifuc.export import SaveExporter
from waifuc.source import ZerochanSource

if __name__ == '__main__':
    s = ZerochanSource('Amiya')
    # the 50 means only need first 50 images
    # if you need to get all images from zerochan,
    # just replace it with 's.export('
    s[:50].export(
        SaveExporter('/data/amiya_zerochan')
    )
