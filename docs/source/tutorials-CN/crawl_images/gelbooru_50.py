from waifuc.export import SaveExporter
from waifuc.source import GelbooruSource

if __name__ == '__main__':
    s = GelbooruSource(['amiya_(arknights)'])
    s[:50].export(
        SaveExporter('/data/amiya_gelbooru')
    )
