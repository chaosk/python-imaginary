from typing import Optional, Dict, Text, Any, Union, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .operations import Operation

IgnoreFailure = bool
OperationWithFailureFlag = Tuple['Operation', IgnoreFailure]
PipelineOperation = Union[
    'Operation',
    OperationWithFailureFlag,
]

RequiredParams = Dict[Text, Any]
OptionalParams = Optional[RequiredParams]
Params = Union[
    OptionalParams,
    RequiredParams,
]

Response = bytes
