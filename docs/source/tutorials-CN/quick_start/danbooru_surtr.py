from waifuc.action import NoMonochromeAction, FilterSimilarAction, \
    TaggingAction, PersonSplitAction, FaceCountAction, FirstNSelectAction, \
    CCIPAction, ModeConvertAction, ClassFilterAction, RandomFilenameAction, AlignMinSizeAction
from waifuc.export import TextualInversionExporter
from waifuc.source import DanbooruSource

if __name__ == '__main__':
    # 将关键词传入，如：'surtr_(arknights)'
    # 注意：对于Danbooru，这里若将'solo'与'surtr_(arknights)'关键词一同传入，
    # 如：['surtr_(arknights)'，'solo']，会使爬取结果更符合预期的单人图像
    # 但并非必须，因为在接下来的流水线中我们会将包含的多人图像处理为单人图像
    s = DanbooruSource(['surtr_(arknights)'])

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
        FaceCountAction(count=1),  # 丢弃没有人脸或有多个人脸的图像
        PersonSplitAction(),  # 将多人图像中每个人物裁出
        FaceCountAction(count=1),  # 丢弃裁出内容中没有人脸或有多个人脸的图像

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
