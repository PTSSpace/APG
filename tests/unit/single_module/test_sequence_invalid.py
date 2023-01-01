import pytest

from textx.exceptions import TextXSyntaxError

from asn1_parser.asn1.validation.asn1_bundle_validator import (
    ASN1ConsistencyError,
)
from asn1_parser.asn1.parser import Asn1Parser

# pylint: disable=line-too-long
# line-too-long warning shows up for the asn modules only
# only other way to disable would be concatenating multiple strings
# to form the modules, but that degrades readability


def test_sequence_extra_comma_one_item():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= SEQUENCE {
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


def test_sequence_extra_comma_two_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= SEQUENCE {
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


def test_sequence_missing_comma_two_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= SEQUENCE {
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


def test_sequence_missing_comma_three_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= SEQUENCE {
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


def test_sequence_undefined_types():
    input_asn = """
Module-test-sequence-undefined-types DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= SEQUENCE {
        my-fruit Fruits-t,
        my-drinks Drinks-t
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(ASN1ConsistencyError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == "Type 'Fruits-t' used in 'test-sequence-undefined-types' is not defined"  # noqa: E501
    )


def test_sequence_with_components_not_defined():
    input_asn = """
Module-test-sequence-with-components-not-defined DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Sandbox-ping ::= SEQUENCE {
        primary-header Ccsds-primary-header
            (WITH COMPONENTS {
                packet-version (0),
                packet-identification (TRUE),
                packet-sequence-control (1.23)
            }),
        secondary-header INTEGER(1..3)
    }

    Ccsds-primary-header ::= SEQUENCE {
        packet-version-number INTEGER(0..7),
        packet-identification BOOLEAN,
        packet-sequence-control REAL(0.1 .. 3.1415),
        packet-data-length INTEGER(3..4)
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(ASN1ConsistencyError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == "'packet-version' in 'Sandbox-ping' is not a valid key"
    )


def test_sequence_with_components_type_not_defined():
    input_asn = """
Module-test-sequence-with-components-type-not-defined DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Sandbox-ping ::= SEQUENCE {
        primary-header Ccsds-primary
            (WITH COMPONENTS {
                packet-version-number (0),
                packet-identification (TRUE),
                packet-sequence-control (1.23)
            }),
        secondary-header INTEGER(1..3)
    }

    Ccsds-primary-header ::= SEQUENCE {
        packet-version-number INTEGER(0..7),
        packet-identification BOOLEAN,
        packet-sequence-control REAL(0.1 .. 3.1415),
        packet-data-length INTEGER(3..4)
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(ASN1ConsistencyError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == "Type 'Ccsds-primary' used in 'test-sequence-with-components-type-not-defined' is not defined"  # noqa: E501
    )


def test_sequence_with_components_multiple_not_defined():
    input_asn = """
Module-test-sequence-with-components-multiple-not-defined DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Sandbox-ping ::= SEQUENCE {
        primary-header Ccsds-primary-header
            (WITH COMPONENTS {
                packet-version-number (0),
                packet-identification (WITH COMPONENTS {
                    packet-type (FALSE),
                    sec-hdr-flag-is-present (TRUE),
                    application-process-identifier (136)
                })
            }),
        secondary-header INTEGER(1..3)
    }

    Ccsds-primary-header ::= SEQUENCE {
        packet-version-number INTEGER(0..7),
        packet-identification Packet-identification,
        packet-sequence-control REAL(0.1 .. 3.1415),
        packet-data-length INTEGER(3..4)
    }

    Packet-identification ::= SEQUENCE {
        packet-type-is-cmd BOOLEAN,
        sec-hdr-flag-is-present BOOLEAN,
        application-process-identifier INTEGER(0..2047)
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(ASN1ConsistencyError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == "'packet-type' in 'Sandbox-ping' is not a valid key"
    )


def test_sequence_with_components_multiple_type_not_defined():
    input_asn = """
Module-test-sequence-with-components-multiple-type-not-defined DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Sandbox-ping ::= SEQUENCE {
        primary-header Ccsds-primary
            (WITH COMPONENTS {
                packet-version-number (0),
                packet-identification (WITH COMPONENTS {
                    packet-type-is-cmd (FALSE),
                    sec-hdr-flag-is-present (TRUE),
                    application-process-identifier (136)
                })
            }),
        secondary-header INTEGER(1..3)
    }

    Ccsds-primary-header ::= SEQUENCE {
        packet-version-number INTEGER(0..7),
        packet-identification Packet-identification,
        packet-sequence-control REAL(0.1 .. 3.1415),
        packet-data-length INTEGER(3..4)
    }

    Packet-identification ::= SEQUENCE {
        packet-type-is-cmd BOOLEAN,
        sec-hdr-flag-is-present BOOLEAN,
        application-process-identifier INTEGER(0..2047)
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(ASN1ConsistencyError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == "Type 'Ccsds-primary' used in 'test-sequence-with-components-multiple-type-not-defined' is not defined"  # noqa: E501
    )


# TODO
