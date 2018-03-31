from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Text,
    Tuple,
    Type,
    Union,
)

from .registry import Registry
from .registry import registry as default_registry
from .types import (
    OperationWithFailureFlag,
    PipelineOperation,
)


class Operation:
    name: Text

    def __init_subclass__(
        cls: Type['Operation'],
        registry: Optional[Registry] = None,
        abstract: bool = False,
    ) -> None:
        if registry is None:
            registry = default_registry
        super().__init_subclass__()
        if not abstract:
            registry.register(cls)

    @classmethod
    def _name(cls) -> Text:
        try:
            return cls.name
        except AttributeError:
            return cls.__name__.lower()

    @classmethod
    def _api_name(cls) -> Text:
        return cls._name()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._arguments = expected_attrs = self.__annotations__.keys()
        for key, value in kwargs.items():
            if key not in expected_attrs:
                raise TypeError(f'Unexpected keyword argument \'{key}\'')
            setattr(self, key, value)
        for key in expected_attrs:
            try:
                getattr(self, key)
            except AttributeError:
                raise TypeError(f'Missing required argument \'{key}\'')

    def __repr__(self) -> str:
        repr_attributes = ', '.join(
            f'{key}={repr(getattr(self, key))}' for key in self._arguments
        )
        return f'<{self.__class__.__name__} {repr_attributes}>'

    def value(self) -> dict:
        return {key: getattr(self, key) for key in self._arguments}

    def as_dict(self) -> dict:
        return {
            'operation': self._name(),
            'params': self.value(),
        }


class Crop(Operation):
    width: int
    height: int


class SmartCrop(Crop):
    pass


class Zoom(Crop):
    factor: float


class Pipeline(Operation):
    operations: Iterable[PipelineOperation]

    def pipeline_values(self) -> Iterator[dict]:
        for operation_value in self.operations:
            if isinstance(operation_value, tuple):
                operation, ignore_failure = operation_value
            else:
                operation, ignore_failure = operation_value, False
            yield {
                'operation': operation._name(),
                'params': operation.value(),
                'ignore_failure': ignore_failure,
            }

    def value(self) -> dict:
        return {
            'operations': list(self.pipeline_values()),
        }
