from typing import List, Dict

from asn1_parser.asn1.grammar_elements.array import Array
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.asn1_string import Asn1String
from asn1_parser.asn1.grammar_elements.choice import Choice
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.utils.array import flatten


class ModuleSorter:
    @staticmethod
    def get_definitions_sorted_by_dependency(
        asn1_module: Asn1Module,
    ) -> List[Definitions]:
        defined_list: List[str] = Asn1Module.PREDEFINED_LIST.copy()

        defined_imports = []
        for item_list in asn1_module.get_import_items():
            defined_imports.append(item_list.get_definitions())

        defined_imports_names: List[List[str]] = []
        for definition_str in defined_imports:
            defined_imports_names.append(definition_str)

        defined_imports_names_flatten: List[str] = flatten(
            defined_imports_names
        )

        defined_list.extend(defined_imports_names_flatten)

        defined_list = list(set(defined_list))

        already_defined: List[Definitions] = []

        not_yet_defined: List[
            Definitions
        ] = asn1_module.get_definitions().copy()
        while len(not_yet_defined) > 0:
            # copy(): do not modify something we iterate on
            for definition in not_yet_defined.copy():
                if isinstance(definition, (Sequence, Choice)):
                    is_all_defined = True
                    for seq_item in definition.get_children():
                        type_name = seq_item.get_asn_type().get_type_name()
                        if isinstance(type_name, Array):
                            type_name = type_name.get_asn_type().get_type_name()
                        if isinstance(type_name, Asn1String):
                            type_name = type_name.get_type_name()
                        if type_name not in defined_list:
                            is_all_defined = False
                            break
                    if is_all_defined:
                        already_defined.append(definition)
                        defined_list.append(definition.get_type_name())
                        not_yet_defined.remove(definition)
                elif isinstance(definition, Enumerated):
                    # Enumerated did not use other types, put it directly to
                    # defined list.
                    already_defined.append(definition)
                    defined_list.append(definition.get_type_name())
                    not_yet_defined.remove(definition)
                elif isinstance(definition, SimpleDefinition):
                    # Simple definitions did not use other types, put it
                    # directly to defined list,
                    already_defined.append(definition)
                    defined_list.append(definition.get_type_name())
                    not_yet_defined.remove(definition)
                else:
                    raise NotImplementedError(
                        f"{definition} (of type {type(definition)})"
                    )

        return already_defined

    @staticmethod
    def create_ordered_import_list(
        real_module_list: List[Asn1Module],
    ) -> List[Asn1Module]:
        module_list: List[Asn1Module] = real_module_list.copy()
        module_order: List[Asn1Module] = []
        module_names: List[str] = [
            item.get_module_name() for item in module_list
        ]
        import_names: List[str] = ModuleSorter._get_import_names(module_list)
        while len(module_list):
            for module_index, module_name in enumerate(module_names):
                if module_name not in import_names:
                    module_to_reorder = module_list[module_index]
                    module_order.append(module_to_reorder)
                    module_list.remove(module_to_reorder)
                    module_names.remove(module_to_reorder.get_module_name())

                    # Regenerate import_list, to omit
                    # the file that we just reordered
                    import_names = ModuleSorter._get_import_names(module_list)
        return module_order

    @staticmethod
    def _get_import_names(module_list: List[Asn1Module]) -> List[str]:
        import_list: Dict[Asn1Module, List[str]] = {}

        for module in module_list:
            import_list[module] = [
                imports_module.get_module_name()
                for imports_module in module.get_import_items()
            ]

        return flatten(list(import_list.values()))
