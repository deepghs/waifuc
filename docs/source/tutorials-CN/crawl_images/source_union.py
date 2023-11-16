from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource, ZerochanSource

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

    # 从两个数据源随机爬取60张
    s = (s_db | s_zerochan)[:60]
    s.export(
        SaveExporter('/data/amiya_zerochan')
    )
