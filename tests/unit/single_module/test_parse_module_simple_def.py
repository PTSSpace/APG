from typing import Set

from asn1_parser.asn1.asn1_bundle_builder import ASN1BundleBuilder
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.parser import Asn1Parser

# pylint: disable=W0212


def test_parse_for_simple_defs():
    input_asn = """
Module-test-string DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Number ::= INTEGER(0..7)
    Simple-sequence ::= SEQUENCE {
        number Number
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_defs: Set[str] = ASN1BundleBuilder._parse_for_simple_defs(asn1_model)
    assert len(simple_defs) == 1

    for string in simple_defs:
        assert string == "Number"
