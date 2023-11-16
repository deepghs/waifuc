from waifuc.export import SaveExporter
from waifuc.source import LocalSource

# 逻辑错误用法！！！
if __name__ == '__main__':
    source = LocalSource('/data/mydataset')
    # 当attach方法添加Action处理后未紧随export方法，
    # 若不进行存储则attach中的Action无效！
    source.attach(
        # XXXAction(), #这里用来代表任意一个Action
    )

    # 这！里！导！出！的！source！未！经！处！理！
    source.export(SaveExporter('/data/dstdataset'))

