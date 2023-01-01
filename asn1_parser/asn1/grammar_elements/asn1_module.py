from typing import List, Optional

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.asn1.grammar_elements.definitions import Definitions
from asn1_parser.asn1.grammar_elements.import_item import ImportItem
from asn1_parser.log.logger import Logger


class Asn1Module:
    _logger = Logger(__name__)
    PREDEFINED_LIST = [
        "BOOLEAN",
        "INTEGER",
        "REAL",
        "IA5String",
        "NumericString",
    ]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        module_name: str,
        definitions: List[Definitions],
        comment: Optional[Asn1Comment],
        comment_import: Optional[Asn1Comment],
        import_items: Optional[List[ImportItem]],
        imported_modules: Optional[List["Asn1Module"]] = None,
    ) -> None:
        if imported_modules is None:
            imported_modules = []
        self._module_name = module_name
        self._definitions = definitions
        self._comment = comment
        Asn1Module._logger.debug(f"comment: {self._comment}")
        self._comment_import = comment_import
        self._import_items = import_items
        self._imported_modules: List[Asn1Module] = imported_modules

    def __str__(self) -> str:
        return (
            self._module_name
            + "\n"
            + (len(self._module_name) * "-")
            + "\n"
            + str(self._definitions)
        )

    def pprint(self) -> None:
        print(f"Module: {self._module_name}")
        print("├── Imports")
        if self._import_items is not None:
            for import_item in self._import_items:
                import_item.pprint(1)
        print("├── Definitions")
        for definition_item in self._definitions:
            definition_item.pprint(1)

    def get_module_name(self) -> str:
        return self._module_name

    def get_definitions(self) -> List[Definitions]:
        return self._definitions

    def get_comment(self) -> Optional[Asn1Comment]:
        return self._comment

    def get_comment_import(self) -> Optional[Asn1Comment]:
        return self._comment_import

    def get_import_items(self) -> List[ImportItem]:
        if self._import_items is not None:
            return self._import_items
        return []

    def add_imported_module(self, module: "Asn1Module") -> None:
        # TODO check if object already in list
        # self._imported_modules
        # = list(set(self._imported_modules.extend(modules)))
        self._imported_modules.extend([module])

    def get_imported_modules(self) -> List["Asn1Module"]:  # TODO
        return self._imported_modules

    def get_imported_modules_names(self) -> List[str]:
        return [
            dependency_module.get_module_name()
            for dependency_module in self.get_imported_modules()
        ]
