from waifuc.export import SaveExporter
from waifuc.source import AnimePicturesSource

if __name__ == '__main__':
    s = AnimePicturesSource(['amiya (arknights)'])
    s[:50].export(
        SaveExporter('/data/amiya_animepictures')
    )
