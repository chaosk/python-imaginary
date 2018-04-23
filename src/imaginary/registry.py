from typing import (
    Dict,
    Text,
)

from .types import TypeBaseOperation

__all__ = [
    'Registry',
    'registry',
]


class Registry:
    """Operation registry, populated automatically
    during Operation subclassing.
    """
    _registry: Dict[str, TypeBaseOperation]

    def __init__(self) -> None:
        self._registry = {}

    def __getitem__(self, name: Text) -> TypeBaseOperation:
        return self._registry[name]

    def __contains__(self, name: Text) -> bool:
        return name in self._registry

    def register(self, operation: TypeBaseOperation) -> None:
        name = operation._name()
        if name in self._registry:
            raise KeyError(f'Operation \'{repr(name)}\' is already registered')
        self._registry[name] = operation


# default registry instance
registry: Registry = Registry()
