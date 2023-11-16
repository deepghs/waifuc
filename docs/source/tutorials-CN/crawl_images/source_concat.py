from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource, ZerochanSource

if __name__ == '__main__':
    # 先从Danbooru爬取30张
    s_db = DanbooruSource(
        ['amiya_(arknights)', 'solo'],
        min_size=10000,
    )[:30]

    # 再从Zerochan爬取30张
    s_zerochan = ZerochanSource(
        'Amiya',
        username='your_username',
        password='your_password',
        select='full',
        strict=True,
    )[:30]

    # 合并爬取到的两个数据流
    s = s_db + s_zerochan
    s.export(
        SaveExporter('/data/amiya_2datasources')
    )
