from waifuc.action import BackgroundRemovalAction, FileExtAction
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
    # Remove background for Zerochan images
    s_zerochan = s_zerochan.attach(
        BackgroundRemovalAction()
    )

    # We need 60 images from these 2 sites
    s = (s_zerochan | s_db)[:60]
    s.attach(
        FileExtAction('.png'),  # Use PNG format to save
    ).export(
        SaveExporter('/data/amiya_zerochan')
    )
