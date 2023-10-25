from waifuc.source import AnimePicturesSource
from .base import resp_recorder


@resp_recorder()
def anime_pictures_surtr():
    s1 = AnimePicturesSource(['surtr (arknights)', 'solo'])
    items = list(s1[:10])


@resp_recorder()
def anime_pictures_2girls():
    s1 = AnimePicturesSource(
        ['texas (arknights)', '2girls'],
        denied_tags=['exusiai (arknights)', 'lappland (arknights)']
    )
    items = list(s1[:10])
