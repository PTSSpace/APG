from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair
from asn1_parser.asn1.parser import Asn1Parser


def test_choice_one_item():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= CHOICE {
        a-t BOOLEAN
    }
END
""".lstrip()

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    choice_t = asn1_model.get_definitions()[0].get_children()

    typ = choice_t[0]
    assert isinstance(typ, KeyTypePair)
    assert typ.get_key() == "a-t"
    assert typ.get_asn_type().get_type_name() == "BOOLEAN"


def test_choice_two_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= CHOICE {
        a-t BOOLEAN,
        b-t BOOLEAN
    }
END
""".lstrip()

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    choice_t = asn1_model.get_definitions()[0].get_children()

    for i, k in zip(range(2), ["a-t", "b-t"]):
        typ = choice_t[i]
        assert isinstance(typ, KeyTypePair)
        assert typ.get_key() == k
        assert typ.get_asn_type().get_type_name() == "BOOLEAN"


def test_choice_three_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq-t ::= CHOICE {
        a-t BOOLEAN,
        b-t BOOLEAN,
        c-t BOOLEAN
    }
END
""".lstrip()

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    choice_t = asn1_model.get_definitions()[0].get_children()

    for i, k in zip(range(3), ["a-t", "b-t", "c-t"]):
        typ = choice_t[i]
        assert isinstance(typ, KeyTypePair)
        assert typ.get_key() == k
