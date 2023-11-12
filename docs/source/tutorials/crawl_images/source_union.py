from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource, ZerochanSource

if __name__ == '__main__':
    # Images from Danbooru
    s_db = DanbooruSource(
        ['amiya_(arknights)', 'solo'],
        min_size=10000,
    )

    # Images from Zerochan
    s_zerochan = ZerochanSource(
        'Amiya',
        username='your_username',
        password='your_password',
        select='full',
        strict=True,
    )

    # We need 60 images from these 2 sites
    s = (s_db | s_zerochan)[:60]
    s.export(
        SaveExporter('/data/amiya_zerochan')
    )
