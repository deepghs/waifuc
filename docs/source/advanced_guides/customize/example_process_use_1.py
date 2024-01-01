from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource

s = DanbooruSource(['texas_(arknights)', 'solo'])
s.attach(
    CutHeadAction(),
)[:30].export(SaveExporter('test_texas_head'))
