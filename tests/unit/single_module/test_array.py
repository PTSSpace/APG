from typing import List

# import pytest
from asn1_parser.asn1.grammar_elements.array import Array
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.asn1_type import Asn1Type
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.asn1.parser import Asn1Parser


def test_array():
    input_asn = """
Module-test-array DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Simple-sequence ::= SEQUENCE {
        my-int INTEGER(0..7)
    }

    My-array ::= SEQUENCE (SIZE (8)) OF Simple-sequence
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definition: Sequence = asn1_model.get_definitions()[0]
    assert isinstance(definition, Sequence)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[1]
    my_array_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(my_array_type, Asn1Type)

    the_array: Array = simple_definition.get_asn_type().get_type()
    assert isinstance(the_array, Array)
    assert isinstance(the_array.get_asn_type().get_type_name(), str)
    assert the_array.get_length() == 8
    assert the_array.get_asn_type().get_type_name() == "Simple-sequence"


def test_array_in_sequence():
    input_asn = """
Module-test-array-in-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Simple-sequence ::= SEQUENCE {
        my-int INTEGER(0..7)
    }

    Simple-sequence-with-array ::= SEQUENCE {
        my-array SEQUENCE (SIZE (8)) OF Simple-sequence,
        age INTEGER(0..128)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definition1: Sequence = asn1_model.get_definitions()[0]
    assert isinstance(definition1, Sequence)

    definition2: Sequence = asn1_model.get_definitions()[1]
    assert isinstance(definition2, Sequence)

    seq: List[KeyTypePair] = definition2.get_children()
    assert seq[0].get_key() == "my-array"

    my_array_type: Asn1Type = seq[0].get_asn_type()
    assert isinstance(my_array_type, Asn1Type)

    the_array: Array = seq[0].get_asn_type().get_type()
    assert isinstance(the_array, Array)
    assert isinstance(the_array.get_asn_type().get_type_name(), str)
    assert the_array.get_length() == 8
    assert the_array.get_asn_type().get_type_name() == "Simple-sequence"
    assert seq[1].get_key() == "age"


def test_array_of_integer():
    input_asn = """
Module-test-array-of-integer DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    My-array ::= SEQUENCE (SIZE (8)) OF INTEGER(0..7)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]

    my_array_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(my_array_type, Asn1Type)

    the_array: Array = simple_definition.get_asn_type().get_type()
    assert isinstance(the_array, Array)
    assert isinstance(the_array.get_asn_type().get_type_name(), str)
    assert the_array.get_length() == 8
    assert the_array.get_asn_type().get_type_name() == "INTEGER"
    assert the_array.get_asn_type().get_begin() == 0
    assert the_array.get_asn_type().get_end() == 7
