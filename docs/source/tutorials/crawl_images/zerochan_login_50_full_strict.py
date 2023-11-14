from waifuc.export import SaveExporter
from waifuc.source import ZerochanSource

if __name__ == '__main__':
    s = ZerochanSource(
        'Amiya',
        username='your_username',
        password='your_password',
        select='full',
        strict=True,
    )
    s[:50].export(
        SaveExporter('/data/amiya_zerochan')
    )
