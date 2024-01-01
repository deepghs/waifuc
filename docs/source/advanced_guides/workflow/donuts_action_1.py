from mydonutsstore.action import IcingAction
from mydonutsstore.source import FryingSource

# fry it by myself
source = FryingSource()

# Icing with chocolate, and that is all
source = source.attach(
    IcingAction(flavor='chocolate'),
)

