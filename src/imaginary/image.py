from typing import (
    IO,
    Any,
    Callable,
    Text,
    Type,
)

from .client import Client
from .operations import (
    BaseOperation,
    Pipeline,
)
from .registry import Registry
from .registry import registry as default_registry

__all__ = [
    'Image',
]


class Image:
    """Represents an image that can be then
    manipulated using :class:`~imaginary.operation.Operation` objects

    :param client: Client instance
    :param registry: Registry instance
    :param file: BytesIO-like object representing image file
    """

    client: Client
    registry: Registry
    file: IO[bytes]

    def __init__(
        self,
        client: Client,
        file: IO[bytes],
        registry: Registry = default_registry,
    ) -> None:
        self.client = client
        self.file = file
        self.registry = registry

    def __call__(self, operation: BaseOperation) -> bytes:
        """Executes a given :class:`~imaginary.operation.Operation`
        and returns a resulting image as bytes.

        :param operation: Operation to execute
        """
        value = operation.value()
        return self.client.post(
            operation._api_name(),
            params=value,
            files={
                'file': self.file,
            },
        )

    def __getattr__(self, name: Text) -> Callable:
        """Retrieves :class:`~imaginary.operation.Operation` from
        :attr:`registry` and prepares a closure with said
        :class:`~imaginary.operation.Operation` ready to be executed.

        >>> image.zoom(factor=1.5)

        is equivalent to:

        >>> image(Zoom(factor=1.5))

        :param name: Lowercase operation name
        """
        try:
            operation_class: Type[BaseOperation] = self.registry[name]
        except KeyError as e:
            class_name = self.__class__.__name__
            raise AttributeError(
                f'\'{class_name}\' object has no attribute \'{name}\''
            ) from e

        def inner(*args: Any, **kwargs: Any) -> bytes:
            return self(operation_class(*args, **kwargs))

        return inner

    def pipeline(self, *operations: BaseOperation) -> bytes:
        """Apply multiple operations sequentially in one request.

        :param \*operations: List of :class:`~imaginary.operation.Operation`
                             objects to apply
        """
        return self(Pipeline(operations=operations))
