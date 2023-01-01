from typing import List, Optional, Dict, Set

from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.generators.cfs.module_sorter import ModuleSorter


class ASN1Bundle:
    def __init__(
        self,
        modules: List[Asn1Module],
        simple_defs_used: Dict[str, Set[str]],
    ) -> None:
        self.modules = modules
        self.simple_def_uses: Dict[str, Set[str]] = simple_defs_used

    def get_module(self, module_name: str) -> Optional[Asn1Module]:
        assert len(self.modules) > 0
        for module in self.modules:
            if module.get_module_name() == module_name:
                return module
        return None

    def get_modules(self) -> List[Asn1Module]:
        return self.modules

    def get_modules_ordered(self) -> List[Asn1Module]:
        copy_of_module_list = self.get_modules().copy()
        return ModuleSorter.create_ordered_import_list(copy_of_module_list)

    def get_modules_names(self) -> List[str]:
        return [module.get_module_name() for module in self.modules]

    def get_simple_def_uses(self) -> Dict[str, Set[str]]:
        return self.simple_def_uses
