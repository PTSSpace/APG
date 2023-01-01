import pytest

from asn1_parser.asn1.parser import Asn1Parser


def test_simple_definition_integer_pos_neg():
    input_asn = """
Module-test-simple-definition-integer-pos-neg DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Nint-t ::= INTEGER(1..-1)
END
""".lstrip()  # noqa: E501

    with pytest.raises(ValueError) as value_error:
        Asn1Parser.parse_from_text(input_asn)

    assert str(value_error.value) == "end: -1 is less then begin: 1"


def test_simple_definition_float_pos_neg():
    input_asn = """
Module-test-simple-definition-real-pos-neg DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Nreal-t ::= REAL(1.0 .. -1.2)
END
""".lstrip()  # noqa: E501

    with pytest.raises(ValueError) as value_error:
        Asn1Parser.parse_from_text(input_asn)

    assert str(value_error.value) == "end: -1.2 is less then begin: 1.0"
