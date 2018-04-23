from typing import Optional

import pytest

from imaginary.operations import Operation


@pytest.fixture
def registry():
    from imaginary.registry import Registry
    return Registry()


def test_operations_name(registry):

    class TestOp(Operation, registry=registry):
        pass

    assert TestOp()._name() == 'testop'


def test_operations_api_name(registry):

    class TestOp(Operation, registry=registry):
        pass

    assert TestOp()._api_name() == 'testop'


def test_operations_repr(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: int

    assert repr(TestOp(foo='baz', bar=10)) == "<TestOp foo='baz', bar=10>"


def test_operations_value(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: int

    expected = {
        'foo': 'baz',
        'bar': 10,
    }
    assert TestOp(foo='baz', bar=10).value() == expected


def test_operations_positional_arguments(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: int

    expected = {
        'foo': 'baz',
        'bar': 10,
    }
    assert TestOp('baz', 10).value() == expected


def test_operations_cant_use_positional_argument_for_optional_params(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: Optional[int]

    with pytest.raises(TypeError) as e:
        TestOp('baz', 10)


def test_operations_multiple_values_for_required_param(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: Optional[int]

    with pytest.raises(TypeError) as e:
        TestOp('baz', foo='baz?')


def test_operations_missing_required_argument(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: int

    with pytest.raises(TypeError):
        assert TestOp(foo='baz')


def test_operations_unexpected_argument(registry):

    class TestOp(Operation, registry=registry):
        foo: str
        bar: int

    with pytest.raises(TypeError):
        assert TestOp(foo='baz', bar=1, baz=4.7)


def test_operations_pipeline_value(registry):
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
