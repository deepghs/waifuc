from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource, ZerochanSource

if __name__ == '__main__':
    # First 30 images from Danbooru
    s_db = DanbooruSource(
        ['amiya_(arknights)', 'solo'],
        min_size=10000,
    )[:30]

    # First 30 images from Zerochan
    s_zerochan = ZerochanSource(
        'Amiya',
        username='your_username',
        password='your_password',
        select='full',
        strict=True,
    )[:30]

    # Concatenate these 2 data sources
    s = s_db + s_zerochan
    s.export(
        SaveExporter('/data/amiya_2datasources')
    )
