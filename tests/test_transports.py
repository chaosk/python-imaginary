import pytest
from requests.exceptions import RequestException

from imaginary.exceptions import TransportError
from imaginary.transports import MockTransport, RequestsTransport
from imaginary.types import Response


def test_transports_mock_get():
    transport = MockTransport()
    response = transport.get(
        url='foo',
        params={},
    )
    assert isinstance(response, Response)
    assert response == Response()


def test_transports_mock_post():
    transport = MockTransport()
    response = transport.post(
        url='foo',
        data={},
        files={},
    )
    assert isinstance(response, Response)
    assert response == Response()


def test_transports_requests_get(mocker):
    transport = RequestsTransport()
    get_mock = mocker.patch('requests.get', autospec=True)
    get_mock.return_value.content = bytes()
    response = transport.get(
        url='foo',
        params={},
    )
    assert isinstance(response, Response)


def test_transports_requests_get_fails(mocker):
    transport = RequestsTransport()
    get_mock = mocker.patch('requests.get')
    get_mock.return_value.raise_for_status.side_effect = RequestException()
    with pytest.raises(TransportError):
        transport.get(
            url='foo',
            params={},
        )


def test_transports_requests_post(mocker):
    transport = RequestsTransport()
    post_mock = mocker.patch('requests.post')
    post_mock.return_value.content = bytes()
    response = transport.post(
        url='foo',
        data={},
        files={},
    )
    assert isinstance(response, Response)


def test_transports_requests_post_fails(mocker):
    transport = RequestsTransport()
    post_mock = mocker.patch('requests.post')
    post_mock.return_value.raise_for_status.side_effect = RequestException()
    with pytest.raises(TransportError):
        transport.post(
            url='foo',
            data={},
            files={},
        )
