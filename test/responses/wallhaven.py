from waifuc.source import WallHavenSource
from .base import resp_recorder


@resp_recorder()
def wallhaven_surtr():
    source = WallHavenSource('surtr (arknights)')
    _ = list(source[:20])


@resp_recorder()
def wallhaven_id_105577():
    source = WallHavenSource('id:105577')
    _ = list(source[:20])
