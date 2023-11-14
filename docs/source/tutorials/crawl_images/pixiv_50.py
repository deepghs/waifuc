from waifuc.export import SaveExporter
from waifuc.source import PixivSearchSource

if __name__ == '__main__':
    s = PixivSearchSource(

        'アークナイツ (amiya OR アーミヤ OR 阿米娅)',
        refresh_token='your_pixiv_refresh_token',
    )
    s[:50].export(
        SaveExporter('/data/amiya_pixiv')
    )
