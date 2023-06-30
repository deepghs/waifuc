from contextlib import contextmanager
from typing import Tuple, Optional

from hbutils.reflection import context

WAIFUC_TASK_NAME = 'waifuc_task_name'


@contextmanager
def task_ctx(name: Optional[str]):
    ctx = context()
    names = tuple(ctx.get(WAIFUC_TASK_NAME, None) or ())
    if name:
        with ctx.vars(**{WAIFUC_TASK_NAME: (*names, name)}):
            yield
    else:
        yield


def get_task_names() -> Tuple[str, ...]:
    ctx = context()
    names = tuple(ctx.get(WAIFUC_TASK_NAME, None) or ())
    return names
