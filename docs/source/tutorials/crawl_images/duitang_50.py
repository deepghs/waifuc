from waifuc.export import SaveExporter
from waifuc.source import DuitangSource

if __name__ == '__main__':
    s = DuitangSource('阿米娅')
    s[:50].export(
        SaveExporter('/data/amiya_duitang')
    )
