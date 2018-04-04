import abc
import logging
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


class Transport(abc.ABC):
    """Abstract interface for HTTP calls
    """

    @abc.abstractmethod
    def get(self, url: Text, params: Params) -> Response:
        """
        :param url: URL to call GET with
        :param params: Querystring parameters
        """
        ...

    @abc.abstractmethod
    def post(self, url: Text, data: Params, files: Params) -> Response:
        """
        :param url: URL to call POST with
        :param data: Data sent using multipart/form-data
        :param files: A dictionary mapping form field name to file data
        """
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
