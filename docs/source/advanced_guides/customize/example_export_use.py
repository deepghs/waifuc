from waifuc.action import FilterSimilarAction, TaggingAction
from waifuc.source import DanbooruSource

s = DanbooruSource(['texas_(arknights)', 'solo'])
s.attach(
    FilterSimilarAction(),
    TaggingAction(),
)[:30].export(CsvExporter('test_texas_csv'))
