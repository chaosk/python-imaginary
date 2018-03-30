from io import BytesIO
from typing import (
    Dict,
    IO,
    Optional,
    Text,
    Tuple,
    Type,
    Union,
)
from urllib.parse import urljoin

from .image import Image
from .transports import (
    Transport,
    RequestsTransport,
)

__all__ = [
    'Imaginary',
]


class Imaginary:
    url: Text
    key: Optional[Text]

    def __init__(
        self,
        url: Text,
        key: Optional[Text] = None,
        transport: Transport = RequestsTransport(),
    ) -> None:
        self.url = url
        self.key = key
        self.transport = transport

    def post(self, path: Text, data, files):
        url = urljoin(self.url, path)
        self.transport.post(
            url=url,
            data=data,
            files=files,
        )

    def get(self, path: Text, params=None):
        url = urljoin(self.url, path)
        self.transport.get(
            url=url,
            params=params,
        )

    def health(self):
        return self.get('/health')

    def versions(self):
        return self.get('/')

    def __call__(self, file: IO[bytes]):
        return Image(self, file)

    def from_path(self, path: Text):
        with open(path, 'rb') as file:
            return Image(self, file)

    def from_bytes(self, bytes: bytes):
        with BytesIO(bytes) as file:
            return Image(self, file)
