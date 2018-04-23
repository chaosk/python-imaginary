from imaginary.params import (
    Color,
    EnumParam,
)


def test_enum_param_serialize():
    class Param(EnumParam):
        foo = 1
        bar = 2

    assert Param.foo.serialize() == 1


def test_color_serialize():
    assert Color(1, 2, 3).serialize() == '1,2,3'
