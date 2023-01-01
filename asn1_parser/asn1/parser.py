import os
from typing import List

from textx import metamodel_from_str

from asn1_parser.asn1.grammar import GRAMMAR
from asn1_parser.asn1.grammar_elements.array import Array
from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.asn1_string import Asn1String
from asn1_parser.asn1.grammar_elements.asn1_type import Asn1Type
from asn1_parser.asn1.grammar_elements.choice import Choice
from asn1_parser.asn1.grammar_elements.components_item import (
    ComponentsItemLast,
    ComponentsItemNotLast,
)
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.grammar_elements.enumerated_item import (
    EnumeratedItemLast,
    EnumeratedItemNotLast,
)
from asn1_parser.asn1.grammar_elements.import_item import ImportItem
from asn1_parser.asn1.grammar_elements.key_type_pair import (
    KeyTypePairLast,
    KeyTypePairNotLast,
)
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.asn1.grammar_elements.with_components import WithComponents
from asn1_parser.asn1.processor import (
    check_comment,
    check_enumerated,
    asn1_type,
    model_processor_check_used_components_defined,
    model_processor_check_used_types_defined,
    null_exception_catch,
    str_to_bool,
)
from asn1_parser.log.logger import Logger


class Asn1Parser:
    _logger = Logger(__name__)

    used_classes = [
        Array,
        Asn1Module,
        Asn1Comment,
        Asn1String,
        Asn1Type,
        Choice,
        ComponentsItemNotLast,
        ComponentsItemLast,
        Definitions,
        Enumerated,
        EnumeratedItemNotLast,
        EnumeratedItemLast,
        ImportItem,
        KeyTypePairNotLast,
        KeyTypePairLast,
        Sequence,
        SimpleDefinition,
        WithComponents,
    ]

    _obj_processor = {
        # "Asn1Comment": endianness_to_bool,
        "Asn1Comment": check_comment,
        "Asn1Type": asn1_type,
        "ComponentsItemNotLast": str_to_bool,
        "ComponentsItemLast": str_to_bool,
        "Enumerated": check_enumerated,
        "KeyTypePairNotLast": null_exception_catch,
        "KeyTypePairLast": null_exception_catch,
        "SimpleDefinition": null_exception_catch,
    }

    @classmethod
    def parse_from_files(cls, *input_file_paths: str) -> List[Asn1Module]:
        input_texts = []
        for input_file_path in input_file_paths:
            assert os.path.exists(
                input_file_path
            ), f"File does not exist: {input_file_path}"

            with open(input_file_path, "r", encoding="utf8") as input_file:
                input_texts.append(input_file.read())

        return cls.parse_from_text_multimodule(input_texts=input_texts)

    @classmethod
    def parse_from_text(
        cls, input_text: str, is_multimodule: bool = False
    ) -> Asn1Module:
        cls._logger.debug("parsing ASN.1 string")
        meta_model = metamodel_from_str(GRAMMAR, classes=cls.used_classes)
        meta_model.register_obj_processors(cls._obj_processor)
        meta_model.register_model_processor(
            model_processor_check_used_types_defined
        )
        asn_model: Asn1Module = meta_model.model_from_str(input_text)
        if not is_multimodule:
            model_processor_check_used_components_defined(asn_model)
        return asn_model

    @classmethod
    def parse_from_text_multimodule(
        cls, input_texts: List[str]
    ) -> List[Asn1Module]:
        asn1_modules: List[Asn1Module] = []

        for input_text in input_texts:
            module = cls.parse_from_text(input_text, True)
            asn1_modules.append(module)

        return asn1_modules
