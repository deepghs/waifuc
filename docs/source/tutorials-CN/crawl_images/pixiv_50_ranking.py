from waifuc.export import SaveExporter
from waifuc.source import PixivRankingSource

if __name__ == '__main__':
    s = PixivRankingSource(
        mode='day',  # 选择全年龄日榜
        refresh_token='your_pixiv_refresh_token',
    )
    s[:50].export(
        SaveExporter('/data/pixiv_daily_best')
    )
