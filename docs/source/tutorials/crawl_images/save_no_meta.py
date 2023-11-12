from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource

if __name__ == '__main__':
    s = DanbooruSource(
        ['amiya_(arknights)', 'solo'],
        min_size=10000,
    )[:50]
    s.export(
        SaveExporter('/data/amiya_danbooru_nometa', no_meta=True)
    )
