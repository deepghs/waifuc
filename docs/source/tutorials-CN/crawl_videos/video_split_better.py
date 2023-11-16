from waifuc.action import PersonSplitAction, FilterSimilarAction, FileOrderAction, MinSizeFilterAction, FaceCountAction
from waifuc.export import SaveExporter
from waifuc.source import VideoSource

if __name__ == '__main__':
    source = VideoSource.from_directory('/data/videos')
    source = source.attach(
        # 过滤掉全帧相似的视频片段，
        # 例如片头、片尾
        FilterSimilarAction(),

        # 逐张拆分出每个人物
        PersonSplitAction(),

        # 丢弃没有人脸或有多个人脸的图像
        FaceCountAction(1),

        # 丢弃短边小于320像素的图像
        MinSizeFilterAction(320),

        # 丢弃相似或重复的图像
        FilterSimilarAction(),

        # 按顺序重命名文件，扩展名为'.png'
        FileOrderAction(ext='.png'),
    )
    source.export(
        SaveExporter('/data/dstdataset')
    )
