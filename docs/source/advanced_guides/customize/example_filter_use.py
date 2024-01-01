from waifuc.export import SaveExporter
from waifuc.source import DanbooruSource

s = DanbooruSource(['texas_(arknights)'])
s.attach(
    ComicOnlyAction(),
)[:10].export(SaveExporter('test_texas'))
