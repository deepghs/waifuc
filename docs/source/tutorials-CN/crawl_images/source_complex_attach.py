from waifuc.action import BackgroundRemovalAction, FileExtAction
from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource, ZerochanSource

if __name__ == '__main__':
    # 初始化Danbooru数据源
    s_db = DanbooruSource(
        ['amiya_(arknights)', 'solo'],
        min_size=10000,
    )

    # 初始化Zerochan数据源
    s_zerochan = ZerochanSource(
        'Amiya',
        username='your_username',
        password='your_password',
        select='full',
        strict=True,
    )
    # 对爬取自Zerochan的图像进行去背景处理
    s_zerochan = s_zerochan.attach(
        BackgroundRemovalAction()
    )

    # 从Danbooru数据源与处理后的Zerochan数据源中随机爬取60张
    s = (s_zerochan | s_db)[:60]
    s.attach(
        FileExtAction('.png'),  # 以'.png'扩展名保存图像文件
    ).export(
        SaveExporter('/data/amiya_zerochan')
    )
