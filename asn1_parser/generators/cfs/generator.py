import os
import pathlib
from typing import List, Optional, Union

import cgen
from asn1_parser.asn1.asn1_bundle import ASN1Bundle
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.choice import Choice
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.grammar_elements.import_item import ImportItem
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.asn1.grammar_elements.with_components import WithComponents
from asn1_parser.c_data import CData
from asn1_parser.c_printer import CPrinter, HeaderType
from asn1_parser.cli.cli_arg_parser import GenerateCFSCommandConfig
from asn1_parser.generators.cfs.module_sorter import ModuleSorter
from asn1_parser.generators.generator import Generator
from asn1_parser.log.logger import Logger

# Monkey patching cgen. TODO: reimplement cgen in house or submit PR upstream.
cgen.Struct.struct_attributes = lambda self: "__attribute__((packed))"

ASN1_KEY_CCSDS_PRIMARY = "primary"
ASN1_KEY_CCSDS_VERSION = "packet-version-number"
ASN1_KEY_CCSDS_IDENT = "packet-identification"
ASN1_KEY_CCSDS_TYPE = "packet-type-is-cmd"
ASN1_KEY_CCSDS_SEC_HEADER_FLAG = "sec-hdr-flag-is-present"
ASN1_KEY_CCSDS_APID = "application-process-identifier"


class CFSGenerator(Generator):
    _logger = Logger(__name__)

    @classmethod
    def get_msg_filename(cls, module: Union[Asn1Module, ImportItem]) -> str:
        return (
            CPrinter.asn1_to_c_style_naming(module.get_module_name()) + "_msg"
        )

    @classmethod
    def get_msgids_filename(cls, module: Asn1Module) -> str:
        return (
            CPrinter.asn1_to_c_style_naming(module.get_module_name())
            + "_msgids"
        )

    @classmethod
    def generate_cfs(
        cls, config: GenerateCFSCommandConfig, bundle: ASN1Bundle
    ) -> None:
        output_folder = config.output_dir
        if not os.path.isdir(output_folder):
            pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

        module_list_ordered: List[Asn1Module] = bundle.get_modules_ordered()

        for module in module_list_ordered:
            module_cdata = CData.create_empty()

            # Include

            comment = module.get_comment_import()
            if comment is not None:
                module_cdata.add_include(
                    str(cgen.LineComment(comment.get_comment()))
                )

            simple_definition_list_imported: List[SimpleDefinition] = []
            for imported_module in module.get_imported_modules():
                simple_definition_list_imported.extend(
                    [
                        d
                        for d in imported_module.get_definitions()
                        if isinstance(d, SimpleDefinition)
                    ]
                )

            for module_imported_item in module.get_import_items():
                module_cdata.add_include(
                    str(
                        cgen.Include(
                            cls.get_msg_filename(module_imported_item) + ".h",
                            system=False,
                        )
                    )
                )

            # Definitions

            simple_definition_list: List[SimpleDefinition] = [
                d
                for d in module.get_definitions()
                if isinstance(d, SimpleDefinition)
            ]
            simple_definition_list.extend(simple_definition_list_imported)

            used_simple_defs = bundle.get_simple_def_uses()
            for definition in ModuleSorter.get_definitions_sorted_by_dependency(
                module
            ):
                if isinstance(definition, SimpleDefinition):
                    # is used directly where needed
                    def_type_name = definition.get_type_name()
                    if def_type_name in used_simple_defs:
                        sizes_of_builtins: List[int] = [8, 16, 32, 64]
                        bitfield_or_builtin: str = (
                            "builtin"
                            if definition.get_size_bits() in sizes_of_builtins
                            else "bitfield"
                        )
                        formatted_list_of_modules: str = ", ".join(
                            f"'{module}'"
                            for module in (
                                sorted((used_simple_defs[def_type_name]))
                            )
                        )
                        module_cdata.add_include(
                            f"// NOTE: The simple type '{def_type_name}' has "
                            f"been generated to a C {bitfield_or_builtin} type "
                            f"and is used directly in "
                            f"{formatted_list_of_modules}"
                        )
                elif isinstance(definition, Sequence):
                    sequence_cdata = CFSGenerator._convert_sequence_to_c(
                        simple_definition_list, definition, module
                    )
                    module_cdata.extend_with_cdata(sequence_cdata)
                elif isinstance(definition, Enumerated):
                    enum_cdata = CFSGenerator._convert_enumerated_to_c(
                        definition
                    )
                    module_cdata.extend_with_cdata(enum_cdata)
                elif isinstance(definition, Choice):
                    choice_cdata = CFSGenerator._convert_choice_to_c(definition)
                    module_cdata.extend_with_cdata(choice_cdata)
                else:
                    raise NotImplementedError(
                        f"cFS code generation for '{definition}' not yet "
                        + "implemented."
                    )

            c_printer: CPrinter = CPrinter()

            comment = module.get_comment()
            file_documentation = comment and comment.get_comment()
            if file_documentation:
                module_cdata.set_header_comment(file_documentation)

            # generate one xx_msg.h file per module
            filename_msg = cls.get_msg_filename(module)
            c_printer.print_to_file(
                cdata=module_cdata,
                filename=filename_msg,
                output_folder=output_folder,
                header_type=HeaderType.MSG,
            )

            # generate xx_msgids.h if needed
            filename_msgids = cls.get_msgids_filename(module)
            c_printer.print_to_file(
                cdata=module_cdata,
                filename=filename_msgids,
                output_folder=output_folder,
                header_type=HeaderType.MSGIDS,
            )

    @classmethod
    def _ccsds_primary_header_to_msg_id(cls, components: WithComponents) -> int:
        tmtc_id = 0x0
        for component in components.get_components():
            key = component.get_key()
            value = component.get_value()
            if key == ASN1_KEY_CCSDS_IDENT:
                for inner_component in value.get_components():
                    inner_key = inner_component.get_key()
                    inner_value = inner_component.get_value()

                    id_len = 16  # bit
                    bit_pkt_v = 3
                    bit_type = 1
                    bit_hdr_flag = 1
                    bit_pr_id = 11

                    if inner_key == ASN1_KEY_CCSDS_VERSION:
                        tmtc_id = tmtc_id | (
                            inner_value << (id_len - bit_pkt_v)
                        )
                    elif inner_key == ASN1_KEY_CCSDS_TYPE:
                        tmtc_id = tmtc_id | (
                            inner_value << (id_len - bit_pkt_v - bit_type)
                        )
                    elif inner_key == ASN1_KEY_CCSDS_SEC_HEADER_FLAG:
                        tmtc_id = tmtc_id | (
                            inner_value
                            << (id_len - bit_pkt_v - bit_type - bit_hdr_flag)
                        )
                    elif inner_key == ASN1_KEY_CCSDS_APID:
                        tmtc_id = tmtc_id | (
                            inner_value
                            << (
                                id_len
                                - bit_pkt_v
                                - bit_type
                                - bit_hdr_flag
                                - bit_pr_id
                            )
                        )
                    else:
                        raise Exception(f"Unhandled key '{inner_key}'")
            else:
                raise Exception(f"Unhandled key '{key}'")

        return tmtc_id

    @classmethod
    def _process_with_components(
        cls,
        seq_name: str,
        with_components: WithComponents,
    ) -> List[str]:
        define_list: List[str] = []

        for component in with_components.get_components():
            value = component.get_value()
            if isinstance(value, WithComponents):
                if component.get_key() == ASN1_KEY_CCSDS_PRIMARY:
                    symbol = seq_name.upper() + "_MID"
                    value = cls._ccsds_primary_header_to_msg_id(value)
                    define_list.append(
                        str(cgen.Define(symbol, f"(0x{value:04X})"))
                    )
                else:
                    define_list.extend(
                        cls._process_with_components(
                            seq_name, component.get_value()
                        )
                    )
            else:
                if isinstance(value, bool):
                    value = "true" if value else "false"
                define_list.append(
                    str(
                        cgen.Define(
                            (
                                seq_name
                                + "_"
                                + CPrinter.asn1_to_c_style_naming(
                                    component.get_key()
                                )
                            ).upper(),
                            "(" + str(value) + ")",
                        )
                    )
                    + "\n"
                )
        return define_list

    # override
    @classmethod
    def _with_components_handling(
        cls,
        definition_type_name_c: str,
        seq_item: KeyTypePair,
        module: Optional[Asn1Module],
    ) -> CData:
        cdata: CData = CData.create_empty()

        cdata.extend_with_define_list(
            cls._process_with_components(
                definition_type_name_c,
                seq_item.get_with_components(),
            )
        )

        return cdata
