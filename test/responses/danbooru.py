from waifuc.source import DanbooruSource, SafebooruSource

from .base import resp_recorder


@resp_recorder('danbooru')
def danbooru():
    s1 = DanbooruSource(['1girl', 'solo'])
    items = list(s1[:10])


@resp_recorder('safebooru')
def safebooru():
    s1 = SafebooruSource(['1girl', 'solo'])
    items = list(s1[:10])
