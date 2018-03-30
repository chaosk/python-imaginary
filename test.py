import logging
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

from src.client import Imaginary
from src.exceptions import ImaginaryError
from src.operations import Crop, Zoom
from src.transports import MockTransport


logging.basicConfig(level=logging.INFO)

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

