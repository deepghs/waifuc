from waifuc.action import NoMonochromeAction, FilterSimilarAction, \
    TaggingAction, PersonSplitAction, FaceCountAction, FirstNSelectAction, \
    CCIPAction, ModeConvertAction, ClassFilterAction, RandomFilenameAction, AlignMinSizeAction
from waifuc.export import TextualInversionExporter
from waifuc.source import GcharAutoSource

if __name__ == '__main__':
    # 通过gchar扩展包提供的数据源进行爬取
    # 史尔特尔、42、surtr都是支持的
    s = GcharAutoSource('surtr')

    # 爬取图像，处理它们，然后以给定的格式保存到目录中
    s.attach(
        # 以RGB色彩模式加载图像并将透明背景替换为白色背景
        ModeConvertAction('RGB', 'white'),

        # 图像预过滤
        NoMonochromeAction(),  # 丢弃单色、灰度或素描等单色图像
        ClassFilterAction(['illustration', 'bangumi']),  # 丢弃漫画或3D图像
        # RatingFilterAction(['safe', 'r15']),  # 可选，丢弃非全年龄或R15的图像
        FilterSimilarAction('all'),  # 丢弃相似或重复的图像

        # 人像处理
        FaceCountAction(1),  # 丢弃没有人脸或有多个人脸的图像
        PersonSplitAction(),  # 将多人图像中每个人物裁出
        FaceCountAction(1),  # 丢弃裁出内容中没有人脸或有多个人脸的图像

        # CCIP，丢弃内容为非指定角色的图像
        CCIPAction(),

        # 将短边大于800像素的图像等比例调整至短边为800像素
        AlignMinSizeAction(800),

        # 使用wd14 v2进行标注，如果不需要角色标注，将character_threshold设置为1.01
        TaggingAction(force=True),

        FilterSimilarAction('all'),  # 再次丢弃相似或重复的图像
        FirstNSelectAction(200),  # 当已有200张图像到达此步骤时，停止后继图像处理
        # MirrorAction(),  # 可选，镜像处理图像进行数据增强
        RandomFilenameAction(ext='.png'),  # 随机重命名图像
    ).export(
        # 保存到/data/surtr_dataset目录，可自行更改
        TextualInversionExporter('/data/surtr_dataset')
    )
