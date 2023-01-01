from typing import List

from asn1_parser.asn1.asn1_bundle import ASN1Bundle
from asn1_parser.asn1.asn1_bundle_builder import ASN1BundleBuilder
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.import_item import ImportItem
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.asn1.parser import Asn1Parser

# pylint: disable=line-too-long
# line-too-long warning shows up for the asn modules only
# only other way to disable would be concatenating multiple strings
# to form the modules, but that degrades readability


def test_multi_multiimport():
    input_asn = [
        """
Module-multiimport DEFINITIONS AUTOMATIC TAGS ::= BEGIN

  IMPORTS Uint64-t FROM Module-uint
          Load, Percent FROM Module-real;

  Payload-test ::= SEQUENCE {
    cpu Percent,
    load1 Load,
    free-swap Uint64-t
  }

END
""".lstrip(),
        """
Module-uint DEFINITIONS AUTOMATIC TAGS ::= BEGIN

  Uint64-t ::= INTEGER(0..18446744073709551615)

END
""".lstrip(),  # noqa: E501
        """
Module-real DEFINITIONS AUTOMATIC TAGS ::= BEGIN

  Percent ::= REAL(0.00 .. 100.00)
  Load ::= REAL(0.00 .. 30.00)

END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    asn1_bundle: ASN1Bundle = ASN1BundleBuilder.build(asn1_models)

    assert len(asn1_models) == 3

    # multiimport

    asn_multiimport: Asn1Module = asn1_bundle.get_module("multiimport")
    multiimport_depends_on: List[
        str
    ] = asn_multiimport.get_imported_modules_names()
    assert multiimport_depends_on == ["uint", "real"]
    assert isinstance(asn_multiimport, Asn1Module)

    definitions_multiimport: List[
        Definitions
    ] = asn_multiimport.get_definitions()

    payload: Sequence = definitions_multiimport[0]
    assert payload.get_type_name() == "Payload-test"
    assert isinstance(payload, Sequence)
    payload_seq: List[KeyTypePair] = payload.get_children()
    assert payload_seq[0].get_key() == "cpu"
    assert payload_seq[0].get_asn_type().get_type_name() == "Percent"
    assert payload_seq[1].get_key() == "load1"
    assert payload_seq[1].get_asn_type().get_type_name() == "Load"
    assert payload_seq[2].get_key() == "free-swap"
    assert payload_seq[2].get_asn_type().get_type_name() == "Uint64-t"

    imported_modules: List[Asn1Module] = asn_multiimport.get_imported_modules()
    assert isinstance(imported_modules[0], Asn1Module)
    assert imported_modules[0].get_module_name() == "uint"
    assert isinstance(imported_modules[1], Asn1Module)
    assert imported_modules[1].get_module_name() == "real"

    imported_items: List[ImportItem] = asn_multiimport.get_import_items()
    assert isinstance(imported_items[0], ImportItem)
    assert imported_items[0].get_definitions()[0] == "Uint64-t"
    assert isinstance(imported_items[1], ImportItem)
    assert imported_items[1].get_definitions()[0] == "Load"
    assert imported_items[1].get_definitions()[1] == "Percent"

    # uint
    for model in asn1_models:
        if model.get_module_name() == "uint":
            uint: Asn1Module = model

        if model.get_module_name() == "real":
            real: Asn1Module = model

    uint_depends_on = uint.get_imported_modules()
    assert uint_depends_on == []
    assert isinstance(uint, Asn1Module)

    uint64: SimpleDefinition = uint.get_definitions()[0]
    assert uint64.get_type_name() == "Uint64-t"

    # real
    real_depends_on = real.get_imported_modules()
    assert real_depends_on == []
    assert isinstance(real, Asn1Module)

    definitions_real: List[Definitions] = real.get_definitions()

    percent: SimpleDefinition = definitions_real[0]
    assert percent.get_type_name() == "Percent"
    assert percent.get_asn_type().get_type_name() == "REAL"
    assert percent.get_asn_type().get_begin() == 0.0
    assert percent.get_asn_type().get_end() == 100.0

    load: SimpleDefinition = definitions_real[1]
    assert load.get_type_name() == "Load"
    assert load.get_asn_type().get_type_name() == "REAL"
    assert load.get_asn_type().get_begin() == 0.0
    assert load.get_asn_type().get_end() == 30.0
