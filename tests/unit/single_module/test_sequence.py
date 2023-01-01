from typing import List

from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.components_item import ComponentsItem
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.grammar_elements.with_components import WithComponents
from asn1_parser.asn1.parser import Asn1Parser


def test_sequence_enumerated():
    input_asn = """
Module-test-sequence-enumerated DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        my-fruit Fruits-t,
        my-drinks Drinks-t
    }

    Fruits-t ::= ENUMERATED {
        apple,
        pear,
        peach
    }

    Drinks-t ::= ENUMERATED {
        milk,
        tea
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definitions: List[Definitions] = asn1_model.get_definitions()

    definition_seq: Sequence = definitions[0]
    assert isinstance(definition_seq, Sequence)
    assert definition_seq.get_type_name() == "Seq"

    definition_fruit: Enumerated = definitions[1]
    assert isinstance(definition_fruit, Enumerated)
    assert definition_fruit.get_type_name() == "Fruits-t"

    definition_drinks: Enumerated = definitions[2]
    assert isinstance(definition_drinks, Enumerated)
    assert definition_drinks.get_type_name() == "Drinks-t"


# TODO sequence of
# TODO sequence of sequence

#####
# WITH COMPONENTS
#####


def test_sequence_with_components():
    input_asn = """
Module-test-sequence-with-components DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Sandbox-ping ::= SEQUENCE {
        primary-header Ccsds-primary-header
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

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definitions: List[Definitions] = asn1_model.get_definitions()

    definition_ping: Sequence = definitions[0]
    assert isinstance(definition_ping, Sequence)

    primary_header: KeyTypePair = definition_ping.get_children()[0]
    assert primary_header.get_key() == "primary-header"
    assert (
        primary_header.get_asn_type().get_type_name() == "Ccsds-primary-header"
    )

    with_component: WithComponents = primary_header.get_with_components()
    assert isinstance(with_component, WithComponents)

    component_items: List[ComponentsItem] = with_component.get_components()

    vers_number: ComponentsItem = component_items[0]
    assert isinstance(vers_number, ComponentsItem)
    assert vers_number.get_key() == "packet-version-number"
    assert vers_number.get_value() == 0

    id_number: ComponentsItem = component_items[1]
    assert isinstance(id_number, ComponentsItem)
    assert id_number.get_key() == "packet-identification"
    assert id_number.get_value() is True

    sequ_contr: ComponentsItem = component_items[2]
    assert isinstance(sequ_contr, ComponentsItem)
    assert sequ_contr.get_key() == "packet-sequence-control"
    assert sequ_contr.get_value() == 1.23


def test_sequence_with_components_multiple():
    input_asn = """
Module-test-sequence-with-components-multiple DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Sandbox-ping ::= SEQUENCE {
        primary-header Ccsds-primary-header
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

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definitions: List[Definitions] = asn1_model.get_definitions()

    definition_ping: Sequence = definitions[0]
    assert isinstance(definition_ping, Sequence)

    primary_header: KeyTypePair = definition_ping.get_children()[0]
    assert primary_header.get_key() == "primary-header"
    assert (
        primary_header.get_asn_type().get_type_name() == "Ccsds-primary-header"
    )

    with_component: WithComponents = primary_header.get_with_components()
    assert isinstance(with_component, WithComponents)

    component_items: List[ComponentsItem] = with_component.get_components()

    vers_number: ComponentsItem = component_items[0]
    assert isinstance(vers_number, ComponentsItem)
    assert vers_number.get_key() == "packet-version-number"
    assert vers_number.get_value() == 0

    id_number: ComponentsItem = component_items[1]
    assert isinstance(id_number, ComponentsItem)
    assert id_number.get_key() == "packet-identification"

    inner_with_component: WithComponents = id_number.get_value()
    assert isinstance(inner_with_component, WithComponents)

    inner_with_components: List[
        ComponentsItem
    ] = inner_with_component.get_components()

    pkt_type_is_cmd: ComponentsItem = inner_with_components[0]
    assert isinstance(pkt_type_is_cmd, ComponentsItem)
    assert pkt_type_is_cmd.get_key() == "packet-type-is-cmd"
    assert pkt_type_is_cmd.get_value() is False

    sec_hdr_flag_present: ComponentsItem = inner_with_components[1]
    assert isinstance(sec_hdr_flag_present, ComponentsItem)
    assert sec_hdr_flag_present.get_key() == "sec-hdr-flag-is-present"
    assert sec_hdr_flag_present.get_value() is True

    app_process_id: ComponentsItem = inner_with_components[2]
    assert isinstance(app_process_id, ComponentsItem)
    assert app_process_id.get_key() == "application-process-identifier"
    assert app_process_id.get_value() == 136


def test_sequence_one_item():
    input_asn = """
Module-test-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        a INTEGER(0..255)
    }
END
""".lstrip()

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    seq_t = asn1_model.get_definitions()[0].get_children()

    typ = seq_t[0]
    assert isinstance(typ, KeyTypePair)
    assert typ.get_key() == "a"
    assert typ.get_asn_type().get_type_name() == "INTEGER"


def test_sequence_two_items():
    input_asn = """
Module-test-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        a INTEGER(0..255),
        b INTEGER(0..255)
    }
END
""".lstrip()

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    seq_t = asn1_model.get_definitions()[0].get_children()

    for i, k in zip(range(2), ["a", "b"]):
        typ = seq_t[i]
        assert isinstance(typ, KeyTypePair)
        assert typ.get_key() == k
        assert typ.get_asn_type().get_type_name() == "INTEGER"


def test_sequence_three_items():
    input_asn = """
Module-test-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        a INTEGER(0..255),
        b INTEGER(0..255),
        c INTEGER(0..255)
    }
END
""".lstrip()

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    seq_t = asn1_model.get_definitions()[0].get_children()

    for i, k in zip(range(3), ["a", "b", "c"]):
        typ = seq_t[i]
        assert isinstance(typ, KeyTypePair)
        assert typ.get_key() == k
        assert typ.get_asn_type().get_type_name() == "INTEGER"


# TODO
