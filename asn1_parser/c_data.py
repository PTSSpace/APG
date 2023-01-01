from typing import Dict, List


class CData:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods
    def __init__(  # pylint: disable=too-many-arguments
        self,
        data: List[str],
        define_list: List[str],
        include_list: List[str],
        init_list: List[str],
        init_list_predef: List[str],
        init_include: str,
        is_stdbool_needed: bool,
        is_stdint_needed: bool,
        header_comment: str,
        binary_init: Dict[str, List[bytes]],
    ) -> None:
        self._data: List[str] = data
        self._define_list: List[str] = define_list
        self._include_list: List[str] = include_list
        self._init_list: List[str] = init_list
        self._init_list_predef: List[str] = init_list_predef
        self._init_include: str = init_include
        self._is_stdbool_needed: bool = is_stdbool_needed
        self._is_stdint_needed: bool = is_stdint_needed
        self._header_comment: str = header_comment
        self._binary_init: Dict[str, List[bytes]] = binary_init

    @staticmethod
    def create_empty() -> "CData":
        return CData(
            data=[],
            define_list=[],
            include_list=[],
            init_list=[],
            init_list_predef=[],
            init_include="",
            is_stdbool_needed=False,
            is_stdint_needed=False,
            header_comment="",
            binary_init={},
        )

    def is_stdbool_needed(self) -> bool:
        return self._is_stdbool_needed

    def is_stdint_needed(self) -> bool:
        return self._is_stdint_needed

    def get_header_comment(self) -> str:
        return self._header_comment

    def get_include_list(self) -> List[str]:
        return self._include_list

    def get_define_list(self) -> List[str]:
        return self._define_list

    def get_data(self) -> List[str]:
        return self._data

    def get_init_list(self) -> List[str]:
        return self._init_list

    def get_init_list_predef(self) -> List[str]:
        return self._init_list_predef

    def get_init_include(self) -> str:
        return self._init_include

    def get_binary_init(self) -> Dict[str, List[bytes]]:
        return self._binary_init

    def extend_with_cdata(self, other_cdata: "CData") -> None:
        self._data.extend(other_cdata.get_data())
        self.extend_with_define_list(other_cdata.get_define_list())
        self._include_list.extend(other_cdata.get_include_list())
        self._init_list.extend(other_cdata.get_init_list())
        self._init_list_predef.extend(other_cdata.get_init_list_predef())
        # TODO one init_include per file?
        self.set_init_include(other_cdata.get_init_include())
        self.set_stdbool_if_needed(other_cdata.is_stdbool_needed())
        self.set_stdint_if_needed(other_cdata.is_stdint_needed())
        # TODO prevent overriding existing keys
        self._binary_init.update(other_cdata.get_binary_init())

    def add_data(self, data_string: str) -> None:
        self._data.append(data_string)

    def extend_with_define_list(self, define_list: List[str]) -> None:
        self._define_list.extend(define_list)

    def add_init(self, init_str: str) -> None:
        self._init_list.append(init_str)

    def add_init_predef(self, init_predef_str: str) -> None:
        self._init_list_predef.append(init_predef_str)

    def add_include(self, include_string: str) -> None:
        self._include_list.append(include_string)

    def set_stdbool_if_needed(self, is_stdbool_needed: bool) -> None:
        self._is_stdbool_needed = self._is_stdbool_needed or is_stdbool_needed

    def set_stdint_if_needed(self, is_stdint_needed: bool) -> None:
        self._is_stdint_needed = self._is_stdint_needed or is_stdint_needed

    def set_header_comment(self, header_comment: str) -> None:
        self._header_comment = header_comment

    def set_init_include(self, init_include: str) -> None:
        self._init_include = init_include

    def add_binary_init(self, key: str, binary_init_list: List[bytes]) -> None:
        # TODO prevent overriding existing keys
        self.get_binary_init()[key] = binary_init_list
