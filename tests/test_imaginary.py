from io import BytesIO

import pytest

from imaginary import Imaginary
from imaginary.image import Image
from imaginary.transports import MockTransport


@pytest.fixture
def imaginary():
    return Imaginary(
        url='http://test.invalid',
        transport=MockTransport(),
    )


def test_imaginary_health(imaginary, mocker):
    mocker.spy(imaginary.client, 'get')
    imaginary.health()
    imaginary.client.get.assert_called_once_with('/health')


def test_imaginary_versions(imaginary, mocker):
    mocker.spy(imaginary.client, 'get')
    imaginary.versions()
    imaginary.client.get.assert_called_once_with('/')


def test_imaginary_make_image(imaginary, mocker):
    assert isinstance(imaginary(mocker.stub()), Image)


def test_imaginary_make_image_from_bytes(imaginary, mocker):
    bytes_ = bytes()
    image = imaginary.from_bytes(bytes_)
    assert isinstance(image, Image)
    assert image.file.read() == bytes_


def test_imaginary_make_image_from_path(imaginary, mocker):
    mocker.patch('builtins.open', return_value=BytesIO())
    image = imaginary.from_path('abc.png')
    assert isinstance(image, Image)
