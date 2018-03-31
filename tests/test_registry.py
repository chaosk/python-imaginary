import pytest

from imaginary.operations import Operation


@pytest.fixture
def registry():
    from imaginary.registry import Registry
    return Registry()


def test_register(registry):

    class TestOp(Operation, registry=registry):
        pass

    assert TestOp._name() in registry
    assert registry[TestOp._name()]


def test_abstract_operation_not_registered(registry):

    class TestOp(Operation, registry=registry, abstract=True):
        pass

    assert TestOp._name() not in registry


def test_registering_operation_twice_fails(registry):

    class TestOp(Operation, registry=registry):
        pass

    with pytest.raises(KeyError):

        class TestOp(Operation, registry=registry):  # noqa: F811
            pass
