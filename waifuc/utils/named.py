from typing import Optional, List, Any


class NamedObject:
    def _args(self) -> Optional[List[Any]]:
        return None

    def __str__(self):
        return f'{self.__class__.__name__}({", ".join(map(repr, self._args() or []))})'

    def __repr__(self):
        return f'<{self.__class__.__name__} {", ".join(map(repr, self._args() or []))}>'
