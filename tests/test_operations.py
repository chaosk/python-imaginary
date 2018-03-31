import pytest

from imaginary.operations import Operation


@pytest.fixture
def registry():
    from imaginary.registry import Registry
    return Registry()


def test_name(registry):

    class TestOp(Operation, registry=registry):
        pass

    assert TestOp()._name() == 'testop'


def test_api_name(registry):

    class TestOp(Operation, registry=registry):
        pass

    assert TestOp()._api_name() == 'testop'


def test_repr(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: int

    assert repr(TestOp(foo='baz', bar=10)) == "<TestOp foo='baz', bar=10>"


def test_value(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: int

    expected = {
        'foo': 'baz',
        'bar': 10,
    }
    assert TestOp(foo='baz', bar=10).value() == expected


def test_missing_required_argument(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: int

    with pytest.raises(TypeError):
        assert TestOp(foo='baz')


def test_unexpected_argument(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: int

    with pytest.raises(TypeError):
        assert TestOp(foo='baz', bar=1, baz=4.7)


def test_pipeline_value(registry):
    from imaginary.operations import Pipeline

    class TestPipeline(Pipeline, registry=registry):
        pass

    class TestOp(Operation, registry=registry):
        foo: str
        bar: int

    class TestOp2(Operation, registry=registry):
        baz: float

    expected = {
        'operations': [
            {
                'operation': 'testop',
                'params': {
                    'foo': 'baz',
                    'bar': 10,
                },
                'ignore_failure': False,
            },
            {
                'operation': 'testop2',
                'params': {
                    'baz': 21.37,
                },
                'ignore_failure': True,
            },
        ]
    }
    assert TestPipeline(
        operations=[
            TestOp(foo='baz', bar=10),
            (TestOp2(baz=21.37), True),
        ],
    ).value() == expected
