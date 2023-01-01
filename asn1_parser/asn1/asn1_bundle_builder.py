from typing import Dict, Tuple, List, Optional, Union, Set
from collections import Counter

from asn1_parser.asn1.asn1_bundle import ASN1Bundle
from asn1_parser.asn1.grammar_elements.choice import Choice
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.asn1.validation.asn1_bundle_validator import (
    ASN1BundleValidator,
    ASN1ConsistencyError,
)
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.parser import Asn1Parser
from asn1_parser.cli.cli_arg_parser import (
    GenerateBinaryCommandConfig,
    GenerateCCommandConfig,
    GenerateCosmosCommandConfig,
    GenerateCFSCommandConfig,
)


class ASN1BundleBuilder:
    @staticmethod
    def build(modules: List[Asn1Module]) -> ASN1Bundle:
        asn_models: Dict[str, Tuple[Asn1Module, Optional[List[str]]]] = {}
        bundle_simple_defs_used: Dict[str, Set[str]] = {}

        for module in modules:
            ASN1BundleBuilder._filter_dependencies(module, asn_models)
            simple_defs_used_in_module: Set[
                str
            ] = ASN1BundleBuilder._parse_for_simple_defs(module)
            for simple_def in simple_defs_used_in_module:
                if simple_def not in bundle_simple_defs_used:
                    bundle_simple_defs_used[simple_def] = set()
                bundle_simple_defs_used[simple_def].add(
                    module.get_module_name()
                )

        ASN1BundleBuilder._resolve_dependencies(asn_models)

        ASN1BundleBuilder._resolve_types(modules)

        return ASN1Bundle(modules, bundle_simple_defs_used)

    @staticmethod
    def build_from_cfs_config(config: GenerateCFSCommandConfig) -> ASN1Bundle:
        modules: List[Asn1Module] = Asn1Parser.parse_from_files(
            *config.input_paths
        )

        ASN1BundleBuilder._validate_unique_module_names(modules, config)
        bundle = ASN1BundleBuilder.build(modules)
        ASN1BundleValidator.validate_bundle_from_config(config, bundle)

        return bundle

    @staticmethod
    def build_from_cosmos_config(
        config: GenerateCosmosCommandConfig,
    ) -> ASN1Bundle:
        modules: List[Asn1Module] = Asn1Parser.parse_from_files(
            *config.input_paths
        )

        bundle = ASN1BundleBuilder.build(modules)
        ASN1BundleValidator.validate_bundle(bundle)

        return bundle

    @staticmethod
    def build_from_c_config(config: GenerateCCommandConfig) -> ASN1Bundle:
        modules: List[Asn1Module] = Asn1Parser.parse_from_files(
            *config.input_paths
        )

        ASN1BundleBuilder._validate_unique_module_names(modules, config)
        bundle = ASN1BundleBuilder.build(modules)
        ASN1BundleValidator.validate_bundle_from_config(config, bundle)

        return bundle

    @staticmethod
    def build_from_binary_config(
        config: GenerateBinaryCommandConfig,
    ) -> ASN1Bundle:
        modules: List[Asn1Module] = Asn1Parser.parse_from_files(
            *config.input_paths
        )

        ASN1BundleBuilder._validate_unique_module_names(modules, config)
        bundle = ASN1BundleBuilder.build(modules)
        ASN1BundleValidator.validate_bundle_from_config(config, bundle)

        return bundle

    @staticmethod
    def build_from_texts(
        texts: List[str],
    ) -> ASN1Bundle:
        modules: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
            texts
        )

        bundle = ASN1BundleBuilder.build(modules)
        ASN1BundleValidator.validate_bundle(bundle)

        return bundle

    @staticmethod
    def _filter_dependencies(
        module: Asn1Module,
        asn_models: Dict[str, Tuple[Asn1Module, Optional[List[str]]]],
    ) -> None:
        imports = module.get_import_items()
        dependencies: Optional[List[str]] = None
        if imports is not None:
            dependencies = [m.get_module_name() for m in imports]
        asn_models[module.get_module_name()] = (module, dependencies)

    @staticmethod
    def _resolve_dependencies(
        asn_models: Dict[str, Tuple[Asn1Module, Optional[List[str]]]]
    ) -> None:
        module_names = list(asn_models.keys())
        for module_name, module_tuple in asn_models.items():
            module: Asn1Module = module_tuple[0]
            dependencies: Optional[List[str]] = module_tuple[1]
            if dependencies is not None:
                missing = set(dependencies) - set(module_names)
                if missing:
                    raise SyntaxError(
                        f"Module '{module_name}' uses "
                        f"undeclared dependencies {missing}"
                    )
                for dependency in dependencies:
                    module.add_imported_module(asn_models[dependency][0])

    @staticmethod
    def _resolve_types(modules: List[Asn1Module]) -> None:
        """
        Walk all the types and fix the ones which only have the name as a string
        (t.asn1_type.type is None).
        Useful when calling get_size_bits() on a type.
        """
        all_definitions: Dict[str, Definitions] = {}
        for module in modules:
            for definition in module.get_definitions():
                all_definitions[definition.get_type_name()] = definition

        for definition in all_definitions.values():
            if isinstance(definition, Sequence):
                for member in definition.get_children():
                    typ = member.get_asn_type()
                    if typ.get_type() is None:
                        type_def = all_definitions.get(typ.get_type_name())
                        typ.set_type(type_def)

    @staticmethod
    def _validate_unique_module_names(
        module_list: List[Asn1Module],
        config: Union[
            GenerateCFSCommandConfig,
            GenerateBinaryCommandConfig,
            GenerateCCommandConfig,
        ],
    ) -> None:
        error_message: str = ""
        duplicate_modules: List[str] = []
        module_names_list: List[str] = [
            module.get_module_name() for module in module_list
        ]

        counts = Counter(module_names_list)
        duplicate_modules = list(
            set(
                module_name
                for module_name in module_names_list
                if counts[module_name] > 1
            )
        )
        if len(duplicate_modules) == 1:
            error_message = (
                f"The module {duplicate_modules[0]} is found "
                f"multiple times in the bundle"
            )
        elif len(duplicate_modules) > 1:
            error_message = (
                f"The modules {', '.join(duplicate_modules)} are "
                f"found multiple times in the bundle"
            )

        counts = Counter(config.asn1_modules)
        duplicate_modules = list(
            set(
                module_name
                for module_name in config.asn1_modules
                if counts[module_name] > 1
            )
        )
        if len(duplicate_modules) == 1:
            error_message = (
                f"The module {duplicate_modules[0]} is found "
                f"multiple times in the --asn1-modules "
                f"command-line argument"
            )
        elif len(duplicate_modules) > 1:
            error_message = (
                f"The modules {', '.join(duplicate_modules)} are "
                f"found multiple times in the --asn1-modules "
                f"command-line argument"
            )

        if error_message:
            raise ASN1ConsistencyError(error_message)

    @staticmethod
    def _parse_for_simple_defs(module: Asn1Module) -> Set[str]:
        files_simple_defs_used_in: Set[str] = set()
        for definition in module.get_definitions():
            key_type_pairs: List[KeyTypePair] = []
            if isinstance(definition, (Sequence, Choice)):
                key_type_pairs = definition.get_children()
            elif isinstance(definition, (SimpleDefinition, Enumerated)):
                pass
            else:
                raise ASN1ConsistencyError(
                    f"Type {type(definition)} not handled."
                )

            for key_type in key_type_pairs:
                if not key_type.get_with_components():
                    type_name = key_type.get_asn_type().get_type_name()
                    if isinstance(type_name, str):
                        if type_name not in Asn1Module.PREDEFINED_LIST:
                            files_simple_defs_used_in.add(type_name)
        return files_simple_defs_used_in
