import collections.abc
from typing import Optional, List, Any, Union, Mapping, Tuple


class _MapItem:
    def __init__(self, key: str, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f'{self.key}={self.value!r}'


class NamedObject:
    def _args(self) -> Optional[Union[List[Any], Mapping[str, Any], Tuple[List[Any], Mapping[str, Any]]]]:
        return None

    def _args_repr(self):
        _args_values = self._args() or []
        if isinstance(_args_values, list):
            _items = [*_args_values]
        elif isinstance(_args_values, collections.abc.Mapping):
            _items = [_MapItem(key, value) for key, value in _args_values.items()]
        elif isinstance(_args_values, tuple):
            _positionals, _kws = _args_values
            _items = [
                *_positionals,
                *[_MapItem(key, value) for key, value in _kws.items()]
            ]
        else:
            raise TypeError(f'Unknown args type - {_args_values!r}.')

        return ", ".join(map(repr, _items))

    def __str__(self):
        return f'{self.__class__.__name__}({self._args_repr()})'

    def __repr__(self):
        return f'<{self.__class__.__name__} {self._args_repr()}>'
