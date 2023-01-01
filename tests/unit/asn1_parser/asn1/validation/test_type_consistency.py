import pytest

from asn1_parser.asn1.validation.asn1_bundle_validator import (
    ASN1ConsistencyError,
)
from asn1_parser.asn1.parser import Asn1Parser


def test_posix_ranges():
    input_asn = """
Module-test-module DEFINITIONS AUTOMATIC TAGS ::= BEGIN

  Uint8-t ::= INTEGER(0..300)
  Uint16-t ::= INTEGER(0..300)

  Test-seq ::= SEQUENCE {
    field1 Uint8-t,
    field2 Uint16-t
  }
END
""".lstrip()

    with pytest.raises(ASN1ConsistencyError) as key_error:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        key_error.value.args[0]
        == "Range [0 - 300] doesn't match with the used POSIX definition "
        "(Uint8-t)."
    )
