from typing import List

from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.grammar_elements.enumerated_item import EnumeratedItem
from asn1_parser.asn1.parser import Asn1Parser


def test_enumerated_item_no_values():
    input_asn = """
Module-test-enumerated-item-no-values DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple,
        banana
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definition: Enumerated = asn1_model.get_definitions()[0]
    assert isinstance(definition, Enumerated)

    assert definition.get_type_name() == "Enum-t"

    enum: List[EnumeratedItem] = definition.get_enum()

    assert enum[0].get_key() == "carrot"
    assert enum[0].get_pos() == 0

    assert enum[1].get_key() == "apple"
    assert enum[1].get_pos() == 1

    assert enum[2].get_key() == "banana"
    assert enum[2].get_pos() == 2


def test_enumerated_item_values():
    input_asn = """
Module-test-enumerated-item-values DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot (2),
        apple (0),
        banana (1)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definition: Enumerated = asn1_model.get_definitions()[0]
    assert isinstance(definition, Enumerated)

    assert definition.get_type_name() == "Enum-t"

    enum: List[EnumeratedItem] = definition.get_enum()

    assert enum[0].get_key() == "apple"
    assert enum[0].get_pos() == 0

    assert enum[1].get_key() == "banana"
    assert enum[1].get_pos() == 1

    assert enum[2].get_key() == "carrot"
    assert enum[2].get_pos() == 2


def test_enumerated_item_mixed_values_0():
    input_asn = """
Module-test-enumerated-item-mixed-values-0 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple (0),
        banana
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definition: Enumerated = asn1_model.get_definitions()[0]
    assert isinstance(definition, Enumerated)

    assert definition.get_type_name() == "Enum-t"

    enum: List[EnumeratedItem] = definition.get_enum()

    assert enum[0].get_key() == "carrot"
    assert enum[0].get_pos() == 0

    assert enum[1].get_key() == "apple"
    assert enum[1].get_pos() == 1

    assert enum[2].get_key() == "banana"
    assert enum[2].get_pos() == 2


def test_enumerated_one_item():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        a-t
    }
END
""".lstrip()

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    enum_t = asn1_model.get_definitions()[0].get_enum()

    typ = enum_t[0]
    assert isinstance(typ, EnumeratedItem)
    assert typ.get_key() == "a-t"


def test_enumerated_two_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        a-t,
        b-t
    }
END
""".lstrip()

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    enum_t = asn1_model.get_definitions()[0].get_enum()

    for i, k in zip(range(2), ["a-t", "b-t"]):
        typ = enum_t[i]
        assert isinstance(typ, EnumeratedItem)
        assert typ.get_key() == k


def test_enumerated_three_items():
    input_asn = """
Module-test DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        a-t,
        b-t,
        c-t
    }
END
""".lstrip()

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    enum_t = asn1_model.get_definitions()[0].get_enum()

    for i, k in zip(range(3), ["a-t", "b-t", "c-t"]):
        typ = enum_t[i]
        assert isinstance(typ, EnumeratedItem)
        assert typ.get_key() == k
