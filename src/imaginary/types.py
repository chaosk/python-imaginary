from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
    Text,
    Tuple,
    Type,
    Union,
)

if TYPE_CHECKING:
    from .operations import Operation

__all__ = [
    'IgnoreFailure',
    'OperationWithFailureFlag',
    'PipelineOperation',
    'TypeOperation',
    'RequiredParams',
    'OptionalParams',
    'Params',
    'Response',
]

IgnoreFailure = bool
OperationWithFailureFlag = Tuple['Operation', IgnoreFailure]
PipelineOperation = Union['Operation', OperationWithFailureFlag, ]
TypeOperation = Type['Operation']

RequiredParams = Dict[Text, Any]
OptionalParams = Optional[RequiredParams]
Params = Union[OptionalParams, RequiredParams, ]

Response = bytes
