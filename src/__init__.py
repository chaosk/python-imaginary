from os import PathLike
from typing import (
    Dict,
    Optional,
    Union,
    Tuple,
    Type,
)
from urllib.parse import urljoin

import requests

from .client import Imaginary
from .exceptions import ImaginaryError
from .operations import Crop, Zoom
from .transports import MockTransport


imaginary = Imaginary('http://imaginary/', transport=MockTransport())

with open('test.png', 'rb') as f:
    image = imaginary(f)

    # GET /health
    imaginary.health()

    try:
        cropped = image.crop(width=123, height=123)
        cropped = image.pipeline(
            Crop(width=100, height=100),
            Zoom(factor=2),
        )
    except ImaginaryError as e:
        print(e)

