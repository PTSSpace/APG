import pytest

from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.asn1_type import Asn1Type
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.asn1.parser import Asn1Parser

#####
# integer
#####


def test_simple_definition_integer_pos_pos():
    input_asn = """
Module-test-simple-definition-integer-pos-pos DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint16-t ::= INTEGER(0..65535)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]
    assert isinstance(simple_definition, SimpleDefinition)

    type_name: str = simple_definition.get_type_name()
    assert type_name == "Uint16-t"

    asn_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(asn_type, Asn1Type)

    begin: int = asn_type.get_begin()
    assert begin == 0

    end: int = asn_type.get_end()
    assert end == 65535


def test_simple_definition_integer_neg_neg():
    input_asn = """
Module-test-simple-definition-integer-neg-neg DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Nint16-t ::= INTEGER(-65535..-1)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]
    assert isinstance(simple_definition, SimpleDefinition)

    type_name: str = simple_definition.get_type_name()
    assert type_name == "Nint16-t"

    asn_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(asn_type, Asn1Type)

    begin: int = asn_type.get_begin()
    assert begin == -65535

    end: int = asn_type.get_end()
    assert end == -1


def test_simple_definition_integer_neg_pos():
    input_asn = """
Module-test-simple-definition-integer-neg-pos DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Nint16-t ::= INTEGER(-65535..0)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]
    assert isinstance(simple_definition, SimpleDefinition)

    type_name: str = simple_definition.get_type_name()
    assert type_name == "Nint16-t"

    asn_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(asn_type, Asn1Type)

    begin: int = asn_type.get_begin()
    assert begin == -65535

    end: int = asn_type.get_end()
    assert end == 0


###


@pytest.mark.skip(reason="not implemented")
def test_simple_definition_integer_pos():
    input_asn = """
Module-test-simple-definition-integer-pos DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint1-t ::= INTEGER(1)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]
    assert isinstance(simple_definition, SimpleDefinition)

    type_name: str = simple_definition.get_type_name()
    assert type_name == "Uint1-t"

    asn_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(asn_type, Asn1Type)

    begin: int = asn_type.get_begin()
    assert begin == 1

    end: int = asn_type.get_end()
    assert end == 1


@pytest.mark.skip(reason="not implemented")
def test_simple_definition_integer_neg():
    input_asn = """
Module-test-simple-definition-integer-neg DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Nint1-t ::= INTEGER(-1)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]
    assert isinstance(simple_definition, SimpleDefinition)

    type_name: str = simple_definition.get_type_name()
    assert type_name == "Nint1-t"

    asn_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(asn_type, Asn1Type)

    begin: int = asn_type.get_begin()
    assert begin == -1

    end: int = asn_type.get_end()
    assert end == -1


#####
# real
#####


def test_simple_definition_real_pos_pos():
    input_asn = """
Module-test-simple-definition-real-pos-pos DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Myreal-t ::= REAL(0.0 .. 3.1415)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]
    assert isinstance(simple_definition, SimpleDefinition)

    type_name: str = simple_definition.get_type_name()
    assert type_name == "Myreal-t"

    asn_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(asn_type, Asn1Type)

    begin: float = asn_type.get_begin()
    assert begin == 0.0

    end: float = asn_type.get_end()
    assert end == 3.1415


def test_simple_definition_real_neg_neg():
    input_asn = """
Module-test-simple-definition-real-neg-neg DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Myreal-t ::= REAL(-3.1415 .. -1.0)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]
    assert isinstance(simple_definition, SimpleDefinition)

    type_name: str = simple_definition.get_type_name()
    assert type_name == "Myreal-t"

    asn_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(asn_type, Asn1Type)

    begin: float = asn_type.get_begin()
    assert begin == -3.1415

    end: float = asn_type.get_end()
    assert end == -1


def test_simple_definition_real_neg_pos():
    input_asn = """
Module-test-simple-definition-real-neg-pos DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Myreal-t ::= REAL(-3.1415 .. 0.0)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]
    assert isinstance(simple_definition, SimpleDefinition)

    type_name: str = simple_definition.get_type_name()
    assert type_name == "Myreal-t"

    asn_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(asn_type, Asn1Type)

    begin: float = asn_type.get_begin()
    assert begin == -3.1415

    end: float = asn_type.get_end()
    assert end == 0.0


###


@pytest.mark.skip(reason="not implemented")
def test_simple_definition_real_pos():
    input_asn = """
Module-test-simple-definition-integer-pos DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Myreal-t ::= REAL(3.1415)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]
    assert isinstance(simple_definition, SimpleDefinition)

    type_name: str = simple_definition.get_type_name()
    assert type_name == "Myreal-t"

    asn_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(asn_type, Asn1Type)

    begin: float = asn_type.get_begin()
    assert begin == 3.1415

    end: float = asn_type.get_end()
    assert end == 3.1415


@pytest.mark.skip(reason="not implemented")
def test_simple_definition_real_neg():
    input_asn = """
Module-test-simple-definition-real-neg DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Myreal-t ::= REAL(-3.1415)
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    simple_definition: SimpleDefinition = asn1_model.get_definitions()[0]
    assert isinstance(simple_definition, SimpleDefinition)

    type_name: str = simple_definition.get_type_name()
    assert type_name == "Myreal-t"

    asn_type: Asn1Type = simple_definition.get_asn_type()
    assert isinstance(asn_type, Asn1Type)

    begin: float = asn_type.get_begin()
    assert begin == -3.1415

    end: float = asn_type.get_end()
    assert end == -3.1415


#####
# bool
#####

# TODO

#####
# string
#####

# TODO
