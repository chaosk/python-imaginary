from io import BytesIO
from typing import (
    IO,
    Text,
)
from urllib.parse import urljoin

from .client import Client
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
    """API Client for Imaginary.
    Used to wrap image files in :class:`~imaginary.image.Image` objects.

    :param url: URL to Imaginary instance
    :param transport: HTTP transport object
    """

    client: Client

    def __init__(
        self,
        url: Text,
        transport: Transport = RequestsTransport(),
    ) -> None:
        self.client = Client(url, transport)

    def health(self) -> Response:
        """Returns health-check information for Imaginary instance
        """
        return self.client.get('/health')

    def versions(self) -> Response:
        """Returns version information for Imaginary instance
        """
        return self.client.get('/')

    def __call__(self, file: IO[bytes]) -> Image:
        """Creates Image instance from a BytesIO-like object

        :param file: BytesIO-like object
        """
        return Image(self.client, file)

    def from_path(self, path: Text) -> Image:
        """Creates Image instance from file located in path.

        :param path: Path to image
        """
        with open(path, 'rb') as file:
            return Image(self.client, file)

    def from_bytes(self, bytes_: bytes) -> Image:
        """Creates Image instance from bytes.

        :param bytes bytes\_: Raw bytes
        """

        file = BytesIO(bytes_)
        return Image(self.client, file)
