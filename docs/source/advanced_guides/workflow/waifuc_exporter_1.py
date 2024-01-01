# NOTE: you already have a source that can provide image items
from waifuc.export import SaveExporter

# save to /my/dataset with images and JSON metadata files
source.exporter(SaveExporter('/my/dataset'))
