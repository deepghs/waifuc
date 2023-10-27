from test.datasources import register_datasource
from waifuc.source import ZerochanSource, DanbooruSource


@register_datasource()
def zerochan_5():
    return ZerochanSource('Surtr (Arknights)', strict=True)[:5]


@register_datasource()
def danbooru_5():
    return DanbooruSource(['surtr_(arknights)', 'solo'])[:5]


@register_datasource()
def zerochan_20():
    return ZerochanSource('Surtr (Arknights)', strict=True)[:20]


@register_datasource()
def danbooru_20():
    return DanbooruSource(['surtr_(arknights)', 'solo'])[:20]
