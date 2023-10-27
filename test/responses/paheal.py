from waifuc.source import PahealSource
from .base import resp_recorder


@resp_recorder()
def paheal_surtr():
    source = PahealSource(['surtr', 'arknights'])
    _ = list(source[:20])
