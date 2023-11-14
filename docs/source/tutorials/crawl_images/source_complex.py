from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource, ZerochanSource, PixivSearchSource

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

    # Images from Pixiv
    s_pixiv = PixivSearchSource(
        'アークナイツ (amiya OR アーミヤ OR 阿米娅)',
        refresh_token='your_pixiv_refresh_token',
    )

    # We need 60 images from these 2 sites
    s = s_zerochan[:50] + (s_db | s_pixiv)[:50]
    s.export(
        SaveExporter('/data/amiya_zerochan')
    )
