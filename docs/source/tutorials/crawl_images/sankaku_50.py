from waifuc.export import SaveExporter
from waifuc.source import SankakuSource

if __name__ == '__main__':
    s = SankakuSource(
        ['amiya_(arknights)'],
        username='your_username',
        password='your_password',
    )
    s[:50].export(
        SaveExporter('/data/amiya_sankaku')
    )
