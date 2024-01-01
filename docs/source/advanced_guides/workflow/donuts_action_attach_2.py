from mydonutsstore.action import IcingAction, JimmiesAction
from mydonutsstore.source import FryingSource

# fry it by myself
source = FryingSource()

# just icing, not completed!
process_source = source.attach(IcingAction(flavor='strawberry'))

# heating, and then put jimmies on donuts
source = source.attach(
    HeatingAction(),  # melting down the ice
    JimmiesAction(),
)
