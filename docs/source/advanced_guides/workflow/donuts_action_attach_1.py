from mydonutsstore.action import IcingAction
from mydonutsstore.source import FryingSource

# fry it by myself
source = FryingSource()

# just icing, not completed!
process_source = source.attach(IcingAction(flavor='strawberry'))
