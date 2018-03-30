from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)

from .registry import registry


class BaseOperation:

    def __init_subclass__(cls, **kwargs):
        _registry = kwargs.get('registry', registry)
        super().__init_subclass__()

        if not kwargs.get('abstract', False):
            _registry.register(cls)

    @classmethod
    def _name(cls):
        return getattr(cls, 'name', cls.__name__.lower())

    @classmethod
    def _api_name(cls):
        return cls._name()

    def __init__(self, *args, **kwargs) -> None:
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
            f'{key}={repr(getattr(self, key))}'
            for key in self._arguments
        )
        return f'<{self.__class__.__name__} {repr_attributes}>'


class Operation(BaseOperation, abstract=True):

    def value(self) -> dict:
        return {
            key: getattr(self, key)
            for key in self._arguments
        }

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


IgnoreFailure = bool
PipelineOperation = Union[
    Operation,
    Tuple[Operation, IgnoreFailure],
]


class Pipeline(Operation):
    operations: List[PipelineOperation]

    def pipeline_values(self):
        for operation in self.operations:
            try:
                operation, ignore_failure = operation
            except (TypeError, ValueError):
                ignore_failure = False
            yield {
                'operation': operation._name(),
                'params': operation.value(),
                'ignore_failure': ignore_failure,
            }

    def value(self) -> dict:
        return {
            'operations': list(self.pipeline_values()),
        }
