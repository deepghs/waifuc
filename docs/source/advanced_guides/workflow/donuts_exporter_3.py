# NOTE: you already have a source that can provide some donuts
from mydonutsstore.exporter import TruckExporter

# place the donuts onto the pickup truck
# which has a bed length of 5.5 feet, width of 5 feet, and height of 1.5 feet.
source.export(TruckExporter(type='pickup', length=5.5, width=5, height=1.5))
