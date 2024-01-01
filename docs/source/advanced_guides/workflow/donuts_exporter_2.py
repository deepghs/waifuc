# NOTE: you already have a source that can provide some donuts
from mydonutsstore.exporter import DozenPackExporter

# hand the dozen of donuts over the customer
source.export(DozenPackExporter())
