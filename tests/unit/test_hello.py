from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.parser import Asn1Parser


def test_001_minimal_doc():
    input_asn = """
Module-enumeration-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN

  Food-t ::= ENUMERATED {
    carrot,
    apple,
    banana
  }

END
""".lstrip()

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)

    assert isinstance(asn1_model, Asn1Module)

    assert len(asn1_model.get_definitions()) == 1

    definition: Enumerated = asn1_model.get_definitions()[0]
    assert isinstance(definition, Enumerated)
