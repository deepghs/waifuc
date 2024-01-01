from mydonutsstore.action import IcingAction, JimmiesAction
from mydonutsstore.source import FryingSource

# fry it by myself
source = FryingSource()

# put jimmies before icing
source = source.attach(
    JimmiesAction(),  # jimmies action will fail
    IcingAction(flavor='strawberry'),
)
