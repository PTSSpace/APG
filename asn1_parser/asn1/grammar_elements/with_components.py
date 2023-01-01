from typing import List, Any

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.asn1.grammar_elements.components_item import ComponentsItem
from asn1_parser.log.logger import Logger


class WithComponents:
    _logger = Logger(__name__)

    def __init__(
        self,
        components: List[ComponentsItem],
        comment: Asn1Comment,
        parent: Any,
    ) -> None:
        self._components = components
        self._comment = comment
        WithComponents._logger.debug(f"comment: {self._comment}")
        self._parent = parent

    def __str__(self) -> str:
        return str(self._components)

    def pprint(self, level: int = 0) -> None:
        for item in self._components:
            assert isinstance(item, ComponentsItem)
            item.pprint(level)

    def get_comment(self) -> Asn1Comment:
        return self._comment

    def get_components(self) -> List[ComponentsItem]:
        return self._components
