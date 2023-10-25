from waifuc.action import NoMonochromeAction, FaceCountAction, HeadCountAction, AlignMinSizeAction, RandomFilenameAction
from waifuc.source import ZerochanSource
from .base import register_datasource


@register_datasource()
def ccip_simple():
    s1 = ZerochanSource('Surtr (Arknights)', strict=True)
    s1 = s1.attach(
        NoMonochromeAction(),
        FaceCountAction(1),
        HeadCountAction(1),
    )[:25]

    s2 = ZerochanSource('Mudrock', strict=True)
    s2 = s2.attach(
        NoMonochromeAction(),
        FaceCountAction(1),
        HeadCountAction(1),
    )[:7]

    return (s1 | s2).attach(
        AlignMinSizeAction(512),
        RandomFilenameAction(ext='.jpg'),
    )


@register_datasource()
def ccip_mudrock():
    return ZerochanSource('Mudrock', strict=True).attach(
        NoMonochromeAction(),
        FaceCountAction(1),
        HeadCountAction(1),
    )[:5]
