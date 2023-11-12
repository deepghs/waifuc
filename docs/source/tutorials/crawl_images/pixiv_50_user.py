from waifuc.export import SaveExporter
from waifuc.source import PixivUserSource

if __name__ == '__main__':
    s = PixivUserSource(
        2864095,  # pixiv user 2864095
        refresh_token='your_pixiv_refresh_token',
    )
    s[:50].export(
        SaveExporter('/data/pixiv_user_misaka_12003')
    )
