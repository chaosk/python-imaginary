from io import BytesIO

import pytest

from imaginary.image import Image
from imaginary.operations import Operation


@pytest.fixture
def client():
    from imaginary.client import Client
    from imaginary.transports import MockTransport
    return Client(
        url='http://test.invalid',
        transport=MockTransport(),
    )


@pytest.fixture
def file():
    return BytesIO()


@pytest.fixture
def registry():
    from imaginary.registry import Registry
    return Registry()


@pytest.fixture
def image(client, file, registry):
    return Image(client=client, file=file, registry=registry)


def test_image_call(image, registry, mocker):

    class TestOp(Operation, registry=registry):
        foo: str

    mocker.patch.object(image.client, 'post')
    image(TestOp(foo=1))

    image.client.post.assert_called_once_with(
        'testop',
        params={
            'foo': 1,
        },
        files={
            'file': image.file,
        },
    )


def test_image_operation_as_attribute(image, registry, mocker):

    class TestOp(Operation, registry=registry):
        foo: str

    mocker.patch.object(image.client, 'post')
    image.testop(foo=1)

    image.client.post.assert_called_once_with(
        'testop',
        params={
            'foo': 1,
        },
        files={
            'file': image.file,
        },
    )


def test_image_unknown_operation_as_attribute_fails(image):
    with pytest.raises(AttributeError):
        image.testop(foo=1)


def test_image_pipeline_attribute(image, registry, mocker):

    class TestOp(Operation, registry=registry):
        foo: str

    class TestOp2(Operation, registry=registry):
        bar: int

    mocker.patch.object(image.client, 'post')

    image.pipeline(
        TestOp(foo='baz'),
        (TestOp2(bar=5), True),
    )

    image.client.post.assert_called_once_with(
        'pipeline',
        params={
            'operations': [
                {
                    'operation': 'testop',
                    'params': {
                        'foo': 'baz',
                    },
                    'ignore_failure': False,
                },
                {
                    'operation': 'testop2',
                    'params': {
                        'bar': 5,
                    },
                    'ignore_failure': True,
                },
            ],
        },
        files={
            'file': image.file,
        },
    )
