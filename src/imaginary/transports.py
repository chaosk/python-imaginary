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

        :raises TransportError: Generic transport failure exception
        """
        ...

    @abc.abstractmethod
    def post(
        self,
        url: Text,
        params: Params = None,
        data: Params = None,
        files: Params = None,
    ) -> Response:
        """
        :param url: URL to call POST with
        :param params: Querystring parameters
        :param data: Data sent using multipart/form-data
        :param files: A dictionary mapping form field name to file data

        :raises TransportError: Generic transport failure exception
        """
        ...


class MockTransport(Transport):

    def get(self, url: Text, params: Params) -> Response:
        logger.info('mocking GET %s (%s)', url, params)
        return Response()

    def post(
        self,
        url: Text,
        params: Params = None,
        data: Params = None,
        files: Params = None,
    ) -> Response:
        logger.info(
            'mocking POST %s (params: %s, data: %s)',
            url,
            params,
            data,
        )
        return Response()


class RequestsTransport(Transport):
    """HTTP tranport for Humans using :mod:`requests`
    """

    def get(self, url: Text, params: Params) -> Response:
        response = requests.get(url, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise TransportError(e) from e
        return response.content

    def post(
        self,
        url: Text,
        params: Params = None,
        data: Params = None,
        files: Params = None,
    ) -> Response:
        response = requests.post(url, params=params, data=data, files=files)
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise TransportError(e) from e
        return response.content
