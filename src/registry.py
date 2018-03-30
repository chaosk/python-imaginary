from typing import (
    Dict,
    Text,
    Type,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from .operations import Operation

__all__ = [
    'Registry',
    'registry',
]


class Registry:
    """Operation registry, populated automatically
    during Operation subclassing.
    """
    _registry: Dict[str, Type['Operation']] = {}

    def __getitem__(self, name: Text) -> Type['Operation']:
        return self._registry[name]

    def register(self, operation: Type['Operation']) -> None:
        name = operation._name()
        if name in self._registry:
            raise KeyError(f'Operation \'{repr(name)}\' is already registered')
        self._registry[name] = operation


# default registry instance
registry: Registry = Registry()
