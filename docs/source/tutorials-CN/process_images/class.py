from waifuc.action import ClassFilterAction
from waifuc.export import SaveExporter
from waifuc.source import LocalSource

if __name__ == '__main__':
    source = LocalSource('/data/raw')
    # 只保留插画或番剧截图图像
    # 支持的类型有'illustration','bangumi','comic','3D'
    source = source.attach(
        ClassFilterAction(['illustration', 'bangumi']),
    )

    source.export(SaveExporter('/data/dstdataset'))
