from asn1_parser.asn1.parser import Asn1Parser
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.asn1_string import Asn1String
from asn1_parser.asn1.grammar_elements.asn1_type import Asn1Type
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.sequence import Sequence


def test_string():
    input_asn = """
Module-test-string DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Simple-sequence ::= SEQUENCE {
        my-string IA5String (SIZE (128))
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definition: Definitions = asn1_model.get_definitions()[0]
    assert isinstance(definition, Sequence)
    assert definition.get_children()[0].get_key() == "my-string"
    the_string_type: Asn1Type = definition.get_children()[0].get_asn_type()
    assert isinstance(the_string_type, Asn1Type)

    the_string: Asn1String = the_string_type.get_type()
    assert isinstance(the_string, Asn1String)
    assert the_string.get_length() == 128
    assert the_string.get_type_name() == "IA5String"


def test_string_numeric():
    input_asn = """
Module-test-string-numeric DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Simple-sequence ::= SEQUENCE {
        my-string NumericString (SIZE (8))
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definition: Definitions = asn1_model.get_definitions()[0]
    assert isinstance(definition, Sequence)
    assert definition.get_children()[0].get_key() == "my-string"

    the_string_type: Asn1Type = definition.get_children()[0].get_asn_type()
    assert isinstance(the_string_type, Asn1Type)

    the_string: Asn1String = the_string_type.get_type()
    assert isinstance(the_string, Asn1String)
    assert isinstance(the_string.get_type_name(), str)
    assert the_string.get_length() == 8
    assert the_string.get_type_name() == "NumericString"
