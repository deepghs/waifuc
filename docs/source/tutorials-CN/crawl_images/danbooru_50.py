from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource

if __name__ == '__main__':
    s = DanbooruSource(['amiya_(arknights)'])
    s[:50].export(
        SaveExporter('/data/amiya_danbooru')
    )
