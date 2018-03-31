from io import BytesIO

import pytest

from imaginary.client import Imaginary
from imaginary.image import Image
from imaginary.transports import MockTransport


@pytest.fixture
def client():
    return Imaginary(
        url='http://test.invalid',
        transport=MockTransport(),
    )


def test_client_get(client, mocker):
    mock = mocker.patch.object(client.transport, 'get')
    client.get('/health')
    mock.assert_called_once_with(
        url='http://test.invalid/health',
        params=None,
    )


def test_client_post(client, mocker):
    mock = mocker.patch.object(client.transport, 'post')
    client.post('/crop', data={'foo': 1}, files={})
    mock.assert_called_once_with(
        url='http://test.invalid/crop',
        data={'foo': 1},
        files={},
    )


def test_client_health(client, mocker):
    mocker.spy(client, 'get')
    client.health()
    client.get.assert_called_once_with('/health')


def test_client_versions(client, mocker):
    mocker.spy(client, 'get')
    client.versions()
    client.get.assert_called_once_with('/')


def test_client_make_image(client, mocker):
    assert isinstance(client(mocker.stub()), Image)


def test_client_make_image_from_bytes(client, mocker):
    bytes_ = bytes()
    image = client.from_bytes(bytes_)
    assert isinstance(image, Image)
    assert image.file.read() == bytes_


def test_client_make_image_from_path(client, mocker):
    mocker.patch('builtins.open', return_value=BytesIO())
    image = client.from_path('abc.png')
    assert isinstance(image, Image)
