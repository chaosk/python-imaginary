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

IgnoreFailure = bool
OperationWithFailureFlag = Tuple['Operation', IgnoreFailure]
PipelineOperation = Union['Operation', OperationWithFailureFlag, ]
TypeOperation = Type['Operation']

RequiredParams = Dict[Text, Any]
OptionalParams = Optional[RequiredParams]
Params = Union[OptionalParams, RequiredParams, ]

Response = bytes
