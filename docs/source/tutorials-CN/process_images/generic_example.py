from waifuc.source import LocalSource
from waifuc.export import SaveExporter


# 正确用法1
if __name__ == '__main__':
    source = LocalSource('/data/mydataset')
    # 当attach方法添加Action处理后紧随export方法
    source.attach(
        # XXXAction(), #这里用来代表任意一个Action
    ).export(SaveExporter('/data/dstdataset'))


# 正确用法2
if __name__ == '__main__':
    source = LocalSource('/data/mydataset')
    # 对调用attach方法添加Action处理后的数据源进行存储
    source = source.attach(
        # XXXAction(), #这里用来代表任意一个Action
    )
    # 此时导出的数据源为Action处理后的数据源
    source.export(SaveExporter('/data/dstdataset'))