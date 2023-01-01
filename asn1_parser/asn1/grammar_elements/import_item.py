from typing import List, Any

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment


class ImportItem:
    def __init__(
        self,
        definitions: List[str],
        module_name: str,
        comment: Asn1Comment,
        parent: Any,
    ) -> None:
        self._definitions = definitions
        self._module_name = module_name
        self._comment = comment
        self._parent = parent

    def __str__(self) -> str:
        return self._module_name + ": {" + str(self._definitions) + "}"

    def pprint(self, level: int = 0) -> None:
        indent = ("│   " * (level >= 1)) + ("    " * (level - 1))
        print(f"{indent}├─ ImportItem: {self._module_name}")
        for item in self._definitions:
            assert isinstance(item, str)
            print(f"{indent}│   ├── {item}")

    def get_definitions(self) -> List[str]:
        return self._definitions

    def get_module_name(self) -> str:
        return self._module_name
