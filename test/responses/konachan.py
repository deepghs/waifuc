from test.responses import resp_recorder
from waifuc.source import KonachanSource, KonachanNetSource, YandeSource


@resp_recorder()
def konachan_surtr():
    source = KonachanSource(['surtr_(arknights)'])
    _ = list(source[:15])


@resp_recorder()
def konachan_2dogs():
    source = KonachanSource(['texas_(arknights)', 'lappland_(arknights)', '2girls'])
    _ = list(source[:20])


@resp_recorder()
def konachan_net_surtr():
    source = KonachanNetSource(['surtr_(arknights)'])
    _ = list(source[:15])


@resp_recorder()
def konachan_net_2dogs():
    source = KonachanNetSource(['texas_(arknights)', 'lappland_(arknights)', '2girls'])
    _ = list(source[:20])


@resp_recorder()
def yande_surtr():
    source = YandeSource(['surtr_(arknights)'])
    _ = list(source[:15])


@resp_recorder()
def yande_2dogs():
    source = YandeSource(['texas_(arknights)', 'lappland_(arknights)'])
    _ = list(source[:20])
