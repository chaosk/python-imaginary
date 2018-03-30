import logging
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Dict,
    Text,
)

import requests

__all__ = [
    'MockTransport',
    'RequestsTransport',
    'Transport',
]

logger = logging.getLogger(__name__)

Params = Dict[Text, Any]


class Transport(ABC):

    @abstractmethod
    def get(self, url: Text, params: Params):
        ...

    @abstractmethod
    def post(self, url: Text, data: Params, files: Params):
        ...


class MockTransport(Transport):

    def get(self, url: Text, params: Params):
        logger.info('mocking GET %(url)s (%(params)s)', url=url, params=params)

    def post(self, url: Text, data: Params, files: Params):
        logger.info('mocking POST %(url)s (%(data)s)', url=url, data=data)


class RequestsTransport(Transport):

    def get(self, url: Text, params: Params):
        return requests.get(url, params=params)

    def post(self, url: Text, data: Params, files: Params):
        return requests.post(url, data=data, files=files)