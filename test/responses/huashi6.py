from test.responses import resp_recorder
from waifuc.source import Huashi6Source


@resp_recorder()
def huashi6_nian():
    source = Huashi6Source('明日方舟 年')
    _ = list(source[:10])
