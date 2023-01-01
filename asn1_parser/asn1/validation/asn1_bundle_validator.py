from typing import List, Union, Dict

from asn1_parser.asn1.asn1_bundle import ASN1Bundle
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.processor import (
    model_processor_check_used_components_defined,
)
from asn1_parser.cli.cli_arg_parser import (
    GenerateBinaryCommandConfig,
    GenerateCCommandConfig,
    GenerateCFSCommandConfig,
)
from asn1_parser.utils.array import flatten


class ASN1ConsistencyError(Exception):
    pass


class ASN1BundleValidator:
    @staticmethod
    def validate_bundle_from_config(
        config: Union[
            GenerateCFSCommandConfig,
            GenerateCCommandConfig,
            GenerateBinaryCommandConfig,
        ],
        bundle: ASN1Bundle,
    ) -> None:
        ASN1BundleValidator.validate_bundle(bundle)
        ASN1BundleValidator.check_missing_modules(config, bundle)

    @staticmethod
    def validate_bundle(bundle: ASN1Bundle) -> None:
        ASN1BundleValidator._check_imported_types_and_check_components(bundle)
        ASN1BundleValidator._check_bundle_for_duplicate_definitions(bundle)

    @staticmethod
    def _check_imported_types_and_check_components(bundle: ASN1Bundle) -> None:
        for asn_module in bundle.get_modules():
            # Checking that imports are defined.
            for imported_module in asn_module.get_imported_modules():
                imp_definitions: List[str] = [
                    definition.get_type_name()
                    for definition in imported_module.get_definitions()
                ]
                imp_types = flatten(
                    [
                        item.get_definitions()
                        for item in asn_module.get_import_items()
                        if item.get_module_name()
                        == imported_module.get_module_name()
                    ]
                )

                undefined = set(imp_types) - set(imp_definitions)
                if undefined:
                    raise ASN1ConsistencyError(
                        f"Error parsing '{asn_module.get_module_name()}': "
                        + f"Imports {undefined} From "
                        + f"'{imported_module.get_module_name()}' not found."
                    )

        # Check components. Create a helper graph with only one module.
        definitions: List[Definitions] = []
        for asn_model in bundle.get_modules():
            definitions.extend(asn_model.get_definitions())
        helper_asn: Asn1Module = Asn1Module(
            "helper", definitions, None, None, None
        )
        model_processor_check_used_components_defined(helper_asn)
        del helper_asn

    @staticmethod
    def _check_bundle_for_duplicate_definitions(
        bundle: ASN1Bundle,
    ) -> None:
        already_defined: Dict[str, str] = {}
        for module in bundle.get_modules():
            for definition in module.get_definitions():
                if isinstance(definition, Definitions):
                    if definition.get_type_name() in already_defined:
                        def_location_in_dict = already_defined[
                            definition.get_type_name()
                        ]
                        # Check to see if the type is defined twice in the same
                        # file, or if it is defined in different files
                        definition_location = (
                            f"{def_location_in_dict}"
                            if def_location_in_dict == module.get_module_name()
                            else f"{def_location_in_dict} and "
                            f"{module.get_module_name()}"
                        )
                        raise ASN1ConsistencyError(
                            f"The type {definition.get_type_name()} "
                            f"was already defined in "
                            f"{definition_location}"
                        )
                    already_defined[
                        definition.get_type_name()
                    ] = module.get_module_name()

    @staticmethod
    def check_missing_modules(
        config: Union[
            GenerateCFSCommandConfig,
            GenerateBinaryCommandConfig,
            GenerateCCommandConfig,
        ],
        bundle: ASN1Bundle,
    ) -> None:
        asn1_module_names_bundle_not_in_config: List[str] = list(
            set(bundle.get_modules_names()) - set(config.asn1_modules)
        )
        missing_modules_in_config = len(asn1_module_names_bundle_not_in_config)
        error_message: str = ""
        if missing_modules_in_config > 0:
            module_plurality = (
                "Module" if missing_modules_in_config == 1 else "Modules"
            )
            literal_plurality = (
                "was" if missing_modules_in_config == 1 else "were"
            )
            error_message = (
                f"{module_plurality} "
                f"{', '.join(asn1_module_names_bundle_not_in_config)} "
                f"{literal_plurality} found in bundle, but {literal_plurality} "
                f"not found in the --asn1-modules command-line argument."
            )
        asn1_module_names_config_not_in_bundle: List[str] = list(
            set(config.asn1_modules) - set(bundle.get_modules_names())
        )
        missing_modules_in_bundle = len(asn1_module_names_config_not_in_bundle)
        if missing_modules_in_bundle > 0:
            module_plurality = (
                "Module" if missing_modules_in_bundle == 1 else "Modules"
            )
            literal_plurality = (
                "was" if missing_modules_in_bundle == 1 else "were"
            )
            error_message = (
                f"{module_plurality} "
                f"{', '.join(asn1_module_names_config_not_in_bundle)} "
                f"{literal_plurality} found in the --asn1-modules command-line "
                f"argument, but {literal_plurality} not found in the bundle."
            )
        if error_message:
            raise ASN1ConsistencyError(
                f"{error_message} \n\n"
                f"Modules found in command-line argument: "
                f"{', '.join(sorted(config.asn1_modules))}"
                f"\n\n"
                f"Modules found in bundle               : "
                f"{', '.join(sorted(bundle.get_modules_names()))}"
            )
