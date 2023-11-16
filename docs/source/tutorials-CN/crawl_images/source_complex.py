from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource, ZerochanSource, PixivSearchSource

if __name__ == '__main__':
    # 初始化Danbooru数据源
    s_db = DanbooruSource(
        ['amiya_(arknights)', 'solo'],
        min_size=10000,
    )

    # 初始化Zerochan数据源
    s_zerochan = ZerochanSource(
        'Amiya',
        username='your_username',
        password='your_password',
        select='full',
        strict=True,
    )

    # 初始化Pixiv数据源
    s_pixiv = PixivSearchSource(
        'アークナイツ (amiya OR アーミヤ OR 阿米娅)',
        refresh_token='your_pixiv_refresh_token',
    )

    # 从构造的数据源爬取共计100张
    s = s_zerochan[:50] + (s_db | s_pixiv)[:50]
    s.export(
        SaveExporter('/data/amiya_zerochan')
    )