from test.responses import resp_recorder
from waifuc.source import DuitangSource


@resp_recorder()
def duitang_nian():
    source = DuitangSource('明日方舟 年')
    _ = list(source[:10])


@resp_recorder()
def duitang_nian_non_strict():
    source = DuitangSource('明日方舟 年', strict=False)
    _ = list(source[:10])
