from io import BytesIO

import pytest

from imaginary.client import Client
from imaginary.image import Image
from imaginary.transports import MockTransport


@pytest.fixture
def client():
    return Client(
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
    client.post('/crop', params={'foo': 1})
    mock.assert_called_once_with(
        url='http://test.invalid/crop',
        params={'foo': 1},
        data=None,
        files=None,
    )
