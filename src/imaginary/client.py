from typing import Text
from urllib.parse import urljoin

from .transports import (
    RequestsTransport,
    Transport,
)
from .types import (
    Params,
    Response,
)

__all__ = [
    'Client',
]


class Client:
    """HTTP client wrapper

    :param url: Base URL for Imaginary service
    :param transport: Transport used for calling Imaginary
    """

    url: Text
    transport: Transport

    def __init__(
        self,
        url: Text,
        transport: Transport = RequestsTransport(),
    ) -> None:
        self.url = url
        self.transport = transport

    def post(self, path: Text, data: Params, files: Params) -> Response:
        """Makes a POST request

        :param path: Request path
        :param data: Form data
        :param files:
        """
        url = urljoin(self.url, path)
        return self.transport.post(
            url=url,
            data=data,
            files=files,
        )

    def get(self, path: Text, params: Params = None) -> Response:
        """Makes a GET request

        :param path: Request path
        :param params: Querystring parameters
        """
        url = urljoin(self.url, path)
        return self.transport.get(
            url=url,
            params=params,
        )
