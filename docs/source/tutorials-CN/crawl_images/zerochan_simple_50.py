from waifuc.export import SaveExporter
from waifuc.source import ZerochanSource

if __name__ == '__main__':
    s = ZerochanSource('Amiya')
    # '[:50]'限制爬取数量为50张，
    # 如果需要全部爬取只需删去即可
    s[:50].export(
        SaveExporter('/data/amiya_zerochan')
    )
