from test.responses import resp_recorder
from waifuc.source import KonachanSource, KonachanNetSource, YandeSource, LolibooruSource, Rule34Source, HypnoHubSource, \
    GelbooruSource, XbooruSource, SafebooruOrgSource, TBIBSource


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


@resp_recorder()
def lolibooru_surtr():
    source = LolibooruSource(['surtr_(arknights)', 'solo'])
    _ = list(source[:15])


@resp_recorder()
def lolibooru_2dogs():
    source = LolibooruSource(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
    _ = list(source[:20])


@resp_recorder()
def rule34_surtr():
    source = Rule34Source(['surtr_(arknights)', 'solo'])
    _ = list(source[:15])


@resp_recorder()
def rule34_2dogs():
    source = Rule34Source(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
    _ = list(source[:20])


@resp_recorder()
def hypnohub_surtr():
    source = HypnoHubSource(['surtr_(arknights)'])
    _ = list(source[:15])


@resp_recorder()
def hypnohub_2dogs():
    source = HypnoHubSource(['texas_(arknights)', 'lappland_(arknights)'])
    _ = list(source[:20])


@resp_recorder()
def gelbooru_surtr():
    source = GelbooruSource(['surtr_(arknights)', 'solo'])
    _ = list(source[:15])


@resp_recorder()
def gelbooru_2dogs():
    source = GelbooruSource(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
    _ = list(source[:20])


@resp_recorder()
def xbooru_surtr():
    source = XbooruSource(['surtr_(arknights)', 'solo'])
    _ = list(source[:15])


@resp_recorder()
def xbooru_2dogs():
    source = XbooruSource(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
    _ = list(source[:20])


@resp_recorder()
def safebooru_org_surtr():
    source = SafebooruOrgSource(['surtr_(arknights)', 'solo'])
    _ = list(source[:15])


@resp_recorder()
def safebooru_org_2dogs():
    source = SafebooruOrgSource(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
    _ = list(source[:20])


@resp_recorder()
def tbib_surtr():
    source = TBIBSource(['surtr_(arknights)', 'solo'])
    _ = list(source[:15])


@resp_recorder()
def tbib_2dogs():
    source = TBIBSource(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
    _ = list(source[:20])
