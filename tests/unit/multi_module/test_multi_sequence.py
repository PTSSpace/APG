from typing import List

from asn1_parser.asn1.asn1_bundle import ASN1Bundle
from asn1_parser.asn1.asn1_bundle_builder import ASN1BundleBuilder
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.components_item import ComponentsItem
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.asn1.grammar_elements.with_components import WithComponents
from asn1_parser.asn1.parser import Asn1Parser

# pylint: disable=line-too-long
# line-too-long warning shows up for the asn modules only
# only other way to disable would be concatenating multiple strings
# to form the modules, but that degrades readability


def test_sequence_import_with_components():
    input_asn = [
        """
Module-sandbox-hk-pc DEFINITIONS AUTOMATIC TAGS ::= BEGIN

  IMPORTS Ccsds-primary-header, Secondary-header FROM Module-tmtc-header;

  Uint64-t ::= INTEGER(0..18446744073709551615) -- 64 bit

  Percent ::= REAL(0.00 .. 100.00) -- [%] 0.00% to 100.00%
  Load ::= REAL(0.00 .. 30.00) -- TODO: check range not to big

  Sandbox-hk-pc-t ::= SEQUENCE {
    primary-header Ccsds-primary-header -- 0x0899
      (WITH COMPONENTS {
        packet-version-number (0),
        packet-identification (WITH COMPONENTS {
          packet-type-is-cmd (FALSE),
          sec-hdr-flag-is-present (TRUE),
          application-process-identifier (153)
        })
      }),
    secondary-header Secondary-header,
    payload Payload-sandbox-hk-pc-t
  }

  Payload-sandbox-hk-pc-t ::= SEQUENCE {
    cpu Percent,
    load1 Load,
    load5 Load,
    load15 Load,
    total-ram Uint64-t, -- [byte]
    free-ram Uint64-t, -- [byte]
    free-swap Uint64-t -- [byte]
  }

END
""".lstrip(),
        """
Module-tmtc-header DEFINITIONS AUTOMATIC TAGS ::= BEGIN -- CCSDS TM/TC header

  Uint16-t ::= INTEGER(0..65535) -- 16 bit, 0x0000 to 0xFFFF
  Uint32-t ::= INTEGER(0..4294967295) -- 32 bit, 0x00000000 to 0xFFFFFFFF

  Ccsds-primary-header ::= SEQUENCE { -- primary header
    packet-version-number INTEGER(0..7), -- 3bit, 0b000 to 0b111
    packet-identification Packet-identification,
    packet-sequence-control Packet-sequence-control,
    packet-data-length Uint16-t
  }

  Packet-identification ::= SEQUENCE {
    packet-type-is-cmd BOOLEAN, -- 1: cmd, 0: tlm
    sec-hdr-flag-is-present BOOLEAN, -- 1: present, 0: absent
    application-process-identifier INTEGER(0..2047) -- 11 bit, 0b00000000000 to 0b11111111111
  }

  Packet-sequence-control ::= SEQUENCE {
    sequence-flags Sequence-flag,
    packet-sequence-count INTEGER(0..16383) -- 14 bit, 0b00000000000000 to 0b11111111111111
  }

  Sequence-flag ::= ENUMERATED { -- 2 bit, 0b00 to 0b11
    continuation-packet-in-sequence (0),
    first-packet-in-sequence (1),
    last-packet-in-sequence (2),
    complete-packet(3)
  }

  Secondary-header ::= SEQUENCE {
    seconds Uint32-t,
    subsecs Uint16-t
  }

END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    asn1_bundle: ASN1Bundle = ASN1BundleBuilder.build(asn1_models)
    assert len(asn1_models) == 2

    # tmtc-header

    asn_tmtc_header: Asn1Module = asn1_bundle.get_module("tmtc-header")
    depends_on_header: List[Asn1Module] = asn_tmtc_header.get_imported_modules()
    assert depends_on_header == []

    # TODO check whole header

    # sandbox-hk-pc

    asn_sandbox_hk_pc: Asn1Module = asn1_bundle.get_module("sandbox-hk-pc")
    depends_on_sandbox: List[
        Asn1Module
    ] = asn_sandbox_hk_pc.get_imported_modules()
    assert depends_on_sandbox[0].get_module_name() == "tmtc-header"
    assert len(depends_on_sandbox) == 1
    assert isinstance(asn_sandbox_hk_pc, Asn1Module)

    definitions: List[Definitions] = asn_sandbox_hk_pc.get_definitions()

    uint64: SimpleDefinition = definitions[0]
    assert uint64.get_type_name() == "Uint64-t"

    percent: SimpleDefinition = definitions[1]
    assert percent.get_type_name() == "Percent"
    assert percent.get_asn_type().get_type_name() == "REAL"
    assert percent.get_asn_type().get_begin() == 0.0
    assert percent.get_asn_type().get_end() == 100.0

    load: SimpleDefinition = definitions[2]
    assert load.get_type_name() == "Load"
    assert load.get_asn_type().get_type_name() == "REAL"
    assert load.get_asn_type().get_begin() == 0.0
    assert load.get_asn_type().get_end() == 30.0

    definition_hk_pc: Sequence = definitions[3]
    assert isinstance(definition_hk_pc, Sequence)

    primary_header: KeyTypePair = definition_hk_pc.get_children()[0]
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

    inner_component_items: List[
        ComponentsItem
    ] = inner_with_component.get_components()

    packet_type_is_cmd: ComponentsItem = inner_component_items[0]
    assert isinstance(packet_type_is_cmd, ComponentsItem)
    assert packet_type_is_cmd.get_key() == "packet-type-is-cmd"
    assert packet_type_is_cmd.get_value() is False

    sec_hdr_flag: ComponentsItem = inner_component_items[1]
    assert isinstance(sec_hdr_flag, ComponentsItem)
    assert sec_hdr_flag.get_key() == "sec-hdr-flag-is-present"
    assert sec_hdr_flag.get_value() is True

    app_id: ComponentsItem = inner_component_items[2]
    assert isinstance(app_id, ComponentsItem)
    assert app_id.get_key() == "application-process-identifier"
    assert app_id.get_value() == 153

    sec_header: KeyTypePair = definition_hk_pc.get_children()[1]
    assert sec_header.get_key() == "secondary-header"
    assert sec_header.get_asn_type().get_type_name() == "Secondary-header"

    payload: KeyTypePair = definition_hk_pc.get_children()[2]
    assert payload.get_key() == "payload"
    assert payload.get_asn_type().get_type_name() == "Payload-sandbox-hk-pc-t"

    # TODO check payload
