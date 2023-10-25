from waifuc.source import DanbooruSource, SafebooruSource, ATFBooruSource, E621Source

from .base import resp_recorder


@resp_recorder('danbooru')
def danbooru():
    s1 = DanbooruSource(['1girl', 'solo'])
    items = list(s1[:10])


@resp_recorder('safebooru')
def safebooru():
    s1 = SafebooruSource(['1girl', 'solo'])
    items = list(s1[:10])


@resp_recorder()
def atfbooru():
    s1 = ATFBooruSource(['scathach_(fate)_(all)'])
    items = list(s1[:10])


@resp_recorder()
def e621_amiya():
    s1 = E621Source(['amiya_(arknights)', 'solo'])
    items = list(s1[:10])


@resp_recorder()
def e621_surtr():
    s1 = E621Source(['surtr_(arknights)', 'solo'])
    items = list(s1[:10])
