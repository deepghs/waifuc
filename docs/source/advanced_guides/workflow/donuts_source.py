from mydonutsstore.source import FryingSource, RefrigeratorSource, NeighborSource

# fry it now
process_source = FryingSource()

# take from the 2nd compartment of your refrigerator
local_source = RefrigeratorSource(compartment_no=2)

# *borrow* from your neighbor
grab_source = NeighborSource(from="Crazy Dave")
