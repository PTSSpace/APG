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
from asn1_parser.cli.cli_arg_parser import GenerateCCommandConfig
from asn1_parser.generators.cfs.module_sorter import ModuleSorter
from asn1_parser.generators.generator import Generator
from asn1_parser.utils.string import lowerize


class CGenerator(Generator):
    @classmethod
    def get_filename(cls, module: Union[Asn1Module, ImportItem]) -> str:
        return CPrinter.asn1_to_c_style_naming(module.get_module_name())

    @classmethod
    def generate_c(
        cls, config: GenerateCCommandConfig, bundle: ASN1Bundle
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
                            cls.get_filename(module_imported_item),
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

            for definition in ModuleSorter.get_definitions_sorted_by_dependency(
                module
            ):
                if isinstance(definition, SimpleDefinition):
                    # is used directly where needed
                    module_cdata.add_include(
                        f"\n// NOTE: {definition.get_type_name()} is embedded "
                        f"directly where it is used. Rationale: Bitfields "
                        f"cannot be typedef'd."
                    )
                elif isinstance(definition, Sequence):
                    sequence_cdata = cls._convert_sequence_to_c(
                        simple_definition_list, definition, module
                    )
                    module_cdata.extend_with_cdata(sequence_cdata)
                elif isinstance(definition, Enumerated):
                    enum_cdata = cls._convert_enumerated_to_c(definition)
                    module_cdata.extend_with_cdata(enum_cdata)
                elif isinstance(definition, Choice):
                    choice_cdata = cls._convert_choice_to_c(definition)
                    module_cdata.extend_with_cdata(choice_cdata)
                else:
                    raise NotImplementedError(
                        f"cFS code generation for '{definition}' not yet "
                        + "implemented."
                    )

            comment = module.get_comment()
            file_documentation = comment and comment.get_comment()
            if file_documentation:
                module_cdata.set_header_comment(file_documentation)

            filename = cls.get_filename(module)
            CPrinter.print_to_file(
                cdata=module_cdata,
                filename=filename,
                output_folder=output_folder,
                header_type=HeaderType.STORED_DATA,
            )

    # override
    @classmethod
    def _with_components_handling(
        cls,
        definition_type_name_c: str,
        seq_item: KeyTypePair,
        module: Optional[Asn1Module],
    ) -> CData:
        if not module:
            raise AttributeError("This method needs the 'module' attribute.")

        cdata: CData = CData.create_empty()

        cdata.add_init(
            cls._process_start_with_component(definition_type_name_c, seq_item)
        )
        cdata.add_init_predef(
            definition_type_name_c
            + " "
            + lowerize(definition_type_name_c)
            + ";"
        )
        filename = cls.get_filename(module)
        cdata.set_init_include(str(cgen.Include(filename + ".h", system=False)))

        return cdata

    @classmethod
    def _process_start_with_component(
        cls,
        seq_name: str,
        seq_item: KeyTypePair,
    ) -> str:
        seq_key: str = seq_item.get_key()
        with_components: WithComponents = seq_item.get_with_components()

        shift_level: int = 1
        return (
            seq_name
            + " "
            + lowerize(seq_name)
            + " = {\n"
            + (shift_level * cls._C_SPACES)
            + "."
            + CPrinter.asn1_to_c_style_naming(seq_key)
            + " = {\n"
            + cls._process_with_components(
                with_components=with_components, shift_level=shift_level + 1
            )
            + (shift_level * cls._C_SPACES)
            + "},\n"
            + "};\n"
        )

    @classmethod
    def _process_with_components(
        cls,
        with_components: WithComponents,
        shift_level: int,
    ) -> str:
        if shift_level < 0:
            raise ValueError("The shift level must be greater or equal 0.")

        init_str: str = ""

        for component in with_components.get_components():
            value = component.get_value()
            if isinstance(value, WithComponents):
                init_str += (
                    (shift_level * cls._C_SPACES)
                    + "."
                    + CPrinter.asn1_to_c_style_naming(component.get_key())
                    + " = {\n"
                    + cls._process_with_components(
                        with_components=component.get_value(),
                        shift_level=shift_level + 1,
                    )
                    + (shift_level * cls._C_SPACES)
                    + "},\n"
                )
            else:
                if isinstance(value, bool):
                    value = 1 if value else 0
                init_str += (
                    (shift_level * cls._C_SPACES)
                    + "."
                    + CPrinter.asn1_to_c_style_naming(component.get_key())
                    + " = "
                    + str(value)
                    + ",\n"
                )

        return init_str
