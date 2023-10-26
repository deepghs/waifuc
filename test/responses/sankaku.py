import os

from waifuc.source import SankakuSource, PostOrder, FileType
from .base import resp_recorder


@resp_recorder()
def sankaku_surtr():
    source = SankakuSource(
        ['surtr_(arknights)', 'solo'],
        order=PostOrder.QUALITY, file_type=FileType.IMAGE,
        username=os.environ['SANKAKU_USERNAME'],
        password=os.environ['SANKAKU_PASSWORD']
    )
    _ = list(source[:20])


@resp_recorder()
def sankaku_2dogs():
    source = SankakuSource(
        ['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'],
        order=PostOrder.QUALITY, file_type=FileType.IMAGE,
        username=os.environ['SANKAKU_USERNAME'],
        password=os.environ['SANKAKU_PASSWORD']
    )
    _ = list(source[:20])


@resp_recorder()
def sankaku_texas_yuri():
    source = SankakuSource(
        ['texas_(arknights)', '2girls', '-lappland_(arknights)', '-exusiai_(arknights)'],
        order=PostOrder.QUALITY, file_type=FileType.IMAGE,
        username=os.environ['SANKAKU_USERNAME'],
        password=os.environ['SANKAKU_PASSWORD']
    )
    _ = list(source[:20])
