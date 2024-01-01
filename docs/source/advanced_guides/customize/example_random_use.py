from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource

s = DanbooruSource(['surtr_(arknights)', 'solo'])
s.attach(
    MyRandomAction(),
)[:30].export(SaveExporter('test_surtr_inv'))
