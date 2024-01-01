from waifuc.action import FilterSimilarAction
from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource

s = DanbooruSource(['texas_(arknights)', 'solo'])
s.attach(
    FilterSimilarAction(),
    CutHeadAction(),
)[:30].export(SaveExporter('test_texas_head'))
