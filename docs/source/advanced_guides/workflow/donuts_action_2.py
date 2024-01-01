from mydonutsstore.action import IcingAction, JimmiesAction
from mydonutsstore.source import FryingSource

# fry it by myself
source = FryingSource()

# Icing with strawberry, and put some jimmies on it
source = source.attach(
    IcingAction(flavor='strawberry'),
    JimmiesAction(),
)
