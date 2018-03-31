import logging
from abc import (
    ABC,
    abstractmethod,
)
from typing import Text

import requests

from .exceptions import TransportError
from .types import (
    Params,
    Response,
)

__all__ = [
    'MockTransport',
    'RequestsTransport',
    'Transport',
]

logger = logging.getLogger(__name__)


class Transport(ABC):

    @abstractmethod
    def get(self, url: Text, params: Params) -> Response:
        ...

    @abstractmethod
    def post(self, url: Text, data: Params, files: Params) -> Response:
        ...


class MockTransport(Transport):

    def get(self, url: Text, params: Params) -> Response:
        logger.info('mocking GET %s (%s)', url, params)
        return Response()

    def post(self, url: Text, data: Params, files: Params) -> Response:
        logger.info('mocking POST %s (%s)', url, data)
        return Response()


class RequestsTransport(Transport):

    def get(self, url: Text, params: Params) -> Response:
        response = requests.get(url, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise TransportError(e) from e
        return response.content

    def post(self, url: Text, data: Params, files: Params) -> Response:
        response = requests.post(url, data=data, files=files)
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise TransportError(e) from e
        return response.content
