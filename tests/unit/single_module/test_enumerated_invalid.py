# pylint: disable=line-too-long

import pytest

from textx.exceptions import TextXSyntaxError

from asn1_parser.asn1.parser import Asn1Parser


def test_enumerated_extra_comma_one_item():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        a-t,
    }
END
""".lstrip()

    with pytest.raises(TextXSyntaxError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == b"Expected NameLower at position (4, 5) => ' a-t,     *} END '."
    )


def test_enumerated_extra_comma_two_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        a-t,
        b-t,
    }
END
""".lstrip()

    with pytest.raises(TextXSyntaxError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == b"Expected NameLower at position (5, 5) => ' b-t,     *} END '."
    )


def test_enumerated_missing_comma_two_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        a-t
        b-t
    }
END
""".lstrip()

    with pytest.raises(TextXSyntaxError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == b"Expected '(' or ',' or '}' at position (4, 9) => 't         *b-t     } '."  # noqa: E501
    )


def test_enumerated_missing_comma_three_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        a-t,
        b-t
        c-t
    }
END
""".lstrip()

    with pytest.raises(TextXSyntaxError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == b"Expected '(' or ',' or '}' at position (5, 9) => 't         *c-t     } '."  # noqa: E501
    )


def test_enumerated_item_mixed_values_1():
    input_asn = """
Module-test-enumerated-item-mixed-values-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple,
        banana (1)
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(IndexError) as index_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        str(index_error.value)
        == "Some indices are not present, multiple times or out of bounds"
    )


def test_enumerated_item_n_values():
    input_asn = """
Module-test-enumerated-item-n-values DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot (2),
        apple (0),
        banana (-1)
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(IndexError) as index_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        str(index_error.value)
        == "Some indices are not present, multiple times or out of bounds"
    )


def test_enumerated_item_false_values():
    input_asn = """
Module-test-enumerated-item-false-values DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot (5),
        apple (0),
        banana (1)
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(IndexError) as index_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        str(index_error.value)
        == "Some indices are not present, multiple times or out of bounds"
    )


def test_enumerated_item_multiple_values_sum():
    input_asn = """
Module-test-enumerated-item-multiple-values-sum DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot (2),
        apple (2),
        banana (1),
        pear (1)
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(IndexError) as index_error:
        Asn1Parser.parse_from_text(input_asn)

    assert str(index_error.value) == "index '2' is defined multiple times"


def test_enumerated_item_multiple_values():
    input_asn = """
Module-test-enumerated-item-multiple-values DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot (1),
        apple (0),
        banana (1)
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(IndexError) as index_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        str(index_error.value)
        == "Some indices are not present, multiple times or out of bounds"
    )
