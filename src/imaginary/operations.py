from typing import (
    Any,
    get_type_hints,
    Iterable,
    Iterator,
    Optional,
    Text,
    Type,
)

from .registry import Registry
from .registry import registry as default_registry
from .params import (
    Color,
    Colorspace,
    Extend,
    Gravity,
    Type as TypeParam,
)
from .types import (
    Params,
    PipelineOperation,
)

__all__ = [
    'Crop',
    'SmartCrop',
    'Resize',
    'Enlarge',
    'Extract',
    'Zoom',
    'Thumbnail',
    'Fit',
    'Rotate',
    'Flip',
    'Flop',
    'Convert',
    'Pipeline',
    'Watermark',
    'Blur',
]


class BaseOperation:
    """Base class for operation
    """

    def __init_subclass__(
        cls: Type['BaseOperation'],
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
        return cls.__name__.lower()

    @classmethod
    def _api_name(cls) -> Text:
        return cls._name()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()
        annotations = get_type_hints(self.__class__)
        expected_attrs = annotations.keys()
        required_attrs = [
            attr for attr, hints in annotations.items()
            if type(None) not in getattr(hints, '__args__', [])
        ]
        used_arguments = []
        for value in args:
            try:
                key = required_attrs.pop(0)
            except IndexError:
                raise TypeError(f'Can\'t use positional argument \'{value}\'')
            setattr(self, key, value)
            used_arguments.append(key)

        for key, value in kwargs.items():
            if key not in expected_attrs:
                raise TypeError(f'Unexpected keyword argument \'{key}\'')
            if key in used_arguments:
                raise TypeError(f'Got multiple values for argument \'{key}\'')
            setattr(self, key, value)
            used_arguments.append(key)

        for key in required_attrs:
            try:
                getattr(self, key)
            except AttributeError:
                raise TypeError(f'Missing required argument \'{key}\'')

        self._arguments = used_arguments

    def __repr__(self) -> str:
        repr_attributes = ', '.join(
            f'{key}={repr(getattr(self, key))}' for key in self._arguments
        )
        return f'<{self.__class__.__name__} {repr_attributes}>'

    def _value(self, key):
        value = getattr(self, key)
        try:
            return value.serialize()
        except AttributeError:
            return value

    def value(self) -> Params:
        return {key: self._value(key) for key in self._arguments}


class Operation(BaseOperation, abstract=True):
    width: Optional[int]
    height: Optional[int]
    quality: Optional[int]
    compression: Optional[int]
    rotate: Optional[int]
    flip: Optional[bool]
    flop: Optional[bool]
    force: Optional[bool]
    norotation: Optional[bool]
    noprofile: Optional[bool]
    stripmeta: Optional[bool]
    type: Optional[TypeParam]
    # file
    # url
    colorspace: Optional[Colorspace]
    field: Optional[Text]
    extend: Optional[Extend]
    background: Optional[Color]
    sigma: Optional[float]
    minampl: Optional[float]
    # sign
    embed: Optional[bool]


class Crop(Operation):
    gravity: Optional[Gravity]


class SmartCrop(Crop):
    pass


class Resize(Operation):
    width: int


class Enlarge(Operation):
    width: int
    height: int


class Extract(Operation):
    top: int
    left: Optional[int]
    areawidth: int
    areaheight: Optional[int]


class Zoom(Operation):
    factor: int


class Thumbnail(Operation):
    pass


class Fit(Operation):
    width: int
    height: int


class Rotate(Operation):
    rotate: int


class Flip(Operation):
    pass


class Flop(Operation):
    pass


class Convert(Operation):
    type: TypeParam


class Pipeline(BaseOperation):
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

    def value(self) -> Params:
        return {
            'operations': list(self.pipeline_values()),
        }


class Watermark(Operation):
    text: Text
    margin: Optional[int]
    dpi: Optional[int]
    textwidth: Optional[int]
    opacity: Optional[float]
    noreplicate: Optional[bool]
    font: Optional[str]
    color: Optional[Color]


class Blur(Operation):
    sigma: int
