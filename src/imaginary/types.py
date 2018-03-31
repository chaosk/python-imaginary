from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
    Text,
    Tuple,
    Union,
)

if TYPE_CHECKING:
    from .operations import Operation

IgnoreFailure = bool
OperationWithFailureFlag = Tuple['Operation', IgnoreFailure]
PipelineOperation = Union['Operation', OperationWithFailureFlag, ]

RequiredParams = Dict[Text, Any]
OptionalParams = Optional[RequiredParams]
Params = Union[OptionalParams, RequiredParams, ]

Response = bytes
