from io import BytesIO
from typing import (
    IO,
    Optional,
    Text,
)
from urllib.parse import urljoin

from .image import Image
from .transports import (
    RequestsTransport,
    Transport,
)
from .types import (
    Params,
    Response,
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

    def post(self, path: Text, data: Params, files: Params) -> Response:
        url = urljoin(self.url, path)
        return self.transport.post(
            url=url,
            data=data,
            files=files,
        )

    def get(self, path: Text, params: Params = None) -> Response:
        url = urljoin(self.url, path)
        return self.transport.get(
            url=url,
            params=params,
        )

    def health(self) -> Response:
        return self.get('/health')

    def versions(self) -> Response:
        return self.get('/')

    def __call__(self, file: IO[bytes]) -> Image:
        return Image(self, file)

    def from_path(self, path: Text) -> Image:
        with open(path, 'rb') as file:
            return Image(self, file)

    def from_bytes(self, bytes: bytes) -> Image:
        with BytesIO(bytes) as file:
            return Image(self, file)
