from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Callable,
    Text,
    Type,
)

from .operations import (
    Operation,
    Pipeline,
)
from .registry import registry as default_registry

if TYPE_CHECKING:
    from .client import Imaginary
    from .registry import Registry

__all__ = [
    'Image',
]


class Image:
    client: 'Imaginary'
    registry: 'Registry'
    file: IO[bytes]

    def __init__(
        self,
        client: 'Imaginary',
        file: IO[bytes],
        registry: 'Registry' = default_registry,
    ) -> None:
        self.client = client
        self.file = file
        self.registry = registry

    def __call__(self, operation: Operation) -> 'Image':
        value = operation.value()
        return self.client.post(
            operation._api_name(),
            data=value,
            files={
                'file': self.file,
            },
        )

    def __getattr__(self, name: Text) -> Callable:
        try:
            operation_class: Type[Operation] = self.registry[name]
        except KeyError as e:
            class_name = self.__class__.__name__
            raise AttributeError(
                f'\'{class_name}\' object has no attribute \'{name}\''
            ) from e

        def inner(*args: Any, **kwargs: Any) -> 'Image':
            return self(operation_class(*args, **kwargs))

        return inner

    def pipeline(self, *operations: Operation) -> 'Image':
        return self(Pipeline(operations=operations))
