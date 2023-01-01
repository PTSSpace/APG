import pytest

from textx.exceptions import TextXSyntaxError

from asn1_parser.asn1.parser import Asn1Parser

# pylint: disable=line-too-long
# line-too-long warning shows up for the asn modules only
# only other way to disable would be concatenating multiple strings
# to form the modules, but that degrades readability


def test_choice_extra_comma_one_item():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= CHOICE {
        a-t BOOLEAN,
    }
END
""".lstrip()

    with pytest.raises(TextXSyntaxError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == b"Expected NameLower at position (4, 5) => 'LEAN,     *} END '."
    )


def test_choice_extra_comma_two_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= CHOICE {
        a-t BOOLEAN,
        b-t BOOLEAN,
    }
END
""".lstrip()

    with pytest.raises(TextXSyntaxError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == b"Expected NameLower at position (5, 5) => 'LEAN,     *} END '."
    )


def test_choice_missing_comma_two_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= CHOICE {
        a-t BOOLEAN
        b-t BOOLEAN
    }
END
""".lstrip()

    with pytest.raises(TextXSyntaxError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == b"Expected ',' or '(WITH COMPONENTS {' or '}' at position (4, 9) => 'N         *b-t BOOLEA'."  # noqa: E501
    )


def test_choice_missing_comma_three_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= CHOICE {
        a-t BOOLEAN,
        b-t BOOLEAN
        c-t BOOLEAN
    }
END
""".lstrip()

    with pytest.raises(TextXSyntaxError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == b"Expected ',' or '(WITH COMPONENTS {' or '}' at position (5, 9) => 'N         *c-t BOOLEA'."  # noqa: E501
    )
