from typing import Any, List, Optional, Union

from textx.exceptions import TextXSyntaxError
from textx.metamodel import TextXMetaModel

from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.asn1_string import Asn1String
from asn1_parser.asn1.grammar_elements.asn1_type import Asn1Type
from asn1_parser.asn1.grammar_elements.choice import Choice
from asn1_parser.asn1.grammar_elements.components_item import ComponentsItem
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.grammar_elements.key_type_pair import KeyTypePair
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.asn1.grammar_elements.with_components import WithComponents

from asn1_parser.utils.array import flatten
from asn1_parser.utils.size import (
    ASN1_POSIX_RANGE,
    DOUBLE_MAX,
    DOUBLE_MIN,
    FLOAT_MAX,
    FLOAT_MIN,
    TypeEnum,
)

#####
# model processors
#####

_PREDEFINED_LIST: List[str] = [
    "BOOLEAN",
    "INTEGER",
    "REAL",
    "IA5String",
    "NumericString",
]


def _check_types_once_defined(model: Asn1Module) -> List[str]:
    # ASN.1 types
    defined_types: List[str] = _PREDEFINED_LIST.copy()
    # get imported types, assume that imported types are defined
    if model.get_import_items() is not None:
        defined_types.extend(
            flatten(
                [items.get_definitions() for items in model.get_import_items()]
            )
        )
    # get new defined types
    defined_types.extend(
        [definition.get_type_name() for definition in model.get_definitions()]
    )
    return defined_types


def model_processor_check_used_types_defined(
    model: Asn1Module, _: TextXMetaModel
) -> None:
    # pylint: disable=import-outside-toplevel
    from asn1_parser.asn1.validation.asn1_bundle_validator import (
        ASN1ConsistencyError,
    )

    defined_types: List[str] = _check_types_once_defined(model)
    for definition in model.get_definitions():
        key_type_pair_list: List[KeyTypePair] = []
        if isinstance(definition, (Sequence, Choice)):
            key_type_pair_list = definition.get_children()
        else:
            pass

        for key_type_pair in key_type_pair_list:
            type_name: str = key_type_pair.get_asn_type().get_type_name()
            if isinstance(type_name, str):
                if type_name not in defined_types:
                    module = model.get_module_name()
                    raise ASN1ConsistencyError(
                        f"Type '{type_name}' used in '{module}' is not defined"
                    )


def model_processor_check_used_components_defined(model: Asn1Module) -> None:
    all_sequences: List[Sequence] = [
        s for s in model.get_definitions() if isinstance(s, Sequence)
    ]
    for definition in model.get_definitions():
        if isinstance(definition, Sequence):
            for seq_item in definition.get_children():
                type_name: str = seq_item.get_asn_type().get_type_name()
                with_component: WithComponents = seq_item.get_with_components()
                _check_with_component(
                    model.get_module_name(),
                    with_component,
                    all_sequences,
                    type_name,
                    definition.get_type_name(),
                )


def _check_with_component(
    module_name: str,
    with_component: WithComponents,
    all_sequences: List[Sequence],
    type_name: str,
    def_type_name: str,
) -> None:

    if with_component is not None:
        # pylint: disable=import-outside-toplevel
        from asn1_parser.asn1.validation.asn1_bundle_validator import (
            ASN1ConsistencyError,
        )

        # find the definition of the sequence used by this WITH COMPONENTS
        sequence: List[Sequence] = [
            s for s in all_sequences if s.get_type_name() == type_name
        ]
        if len(sequence) == 1:
            seq: List[KeyTypePair] = sequence[0].get_children()
            allowed_keys: List[str] = [s.get_key() for s in seq]
            for component in with_component.get_components():
                # go through all components and check whether they are defined
                # or not
                component_key: str = component.get_key()
                if component_key not in allowed_keys:
                    raise ASN1ConsistencyError(
                        f"'{component_key}' in '{def_type_name}' is not a "
                        "valid key"
                    )
                component_value = component.get_value()
                # when a WITH COMPONENTS component has an inner WITH COMPONENTS
                if isinstance(component_value, WithComponents):
                    type_name_inner: str = [
                        s.get_asn_type().get_type_name()
                        for s in seq
                        if s.get_key() == component_key
                    ][0]
                    _check_with_component(
                        module_name,
                        component_value,
                        all_sequences,
                        type_name_inner,
                        def_type_name,
                    )
        elif type_name not in _PREDEFINED_LIST:
            raise ASN1ConsistencyError(
                f"used type '{type_name}' in '{def_type_name}' is not defined"
            )


#####
# object processors
#####


def str_to_bool(model: ComponentsItem) -> None:
    value = model.get_value()
    if isinstance(value, str):
        if value == "TRUE":
            model.set_value(True)
        elif value == "FALSE":
            model.set_value(False)


def asn1_type(model: Asn1Type) -> None:
    # check range

    begin = model.get_begin()
    end = model.get_end()
    if begin is not None and end is not None:
        if end < begin:
            raise ValueError(f"end: {end} is less then begin: {begin}")

    # map to TypeEnum

    type_name: str = model.get_type_name()
    seq_type = model.get_type()

    c_type: Optional[TypeEnum]
    if ASN1_POSIX_RANGE.get(type_name) is not None:
        if type_name.startswith("Uint"):
            c_type = TypeEnum.A_UINT
        elif type_name.startswith("Int"):
            c_type = TypeEnum.A_INT
        elif type_name == "Float":
            c_type = TypeEnum.A_FLOAT
        elif type_name == "Double":
            c_type = TypeEnum.A_DOUBLE
        else:
            c_type = None
    elif type_name == "INTEGER" and begin is not None and end is not None:
        if begin >= 0:
            c_type = TypeEnum.A_UINT
        else:
            # TODO check bounds
            c_type = TypeEnum.A_INT
    elif type_name == "REAL" and begin is not None and end is not None:
        if begin >= FLOAT_MIN and end <= FLOAT_MAX:
            c_type = TypeEnum.A_FLOAT
        elif begin >= DOUBLE_MIN and end <= DOUBLE_MAX:
            c_type = TypeEnum.A_DOUBLE
        else:
            raise FloatingPointError(
                f"{str(begin)} or {str(end)} are out of double range"
            )
    elif type_name == "BOOLEAN":
        c_type = TypeEnum.A_BOOL
    elif isinstance(seq_type, Asn1String):
        c_type = TypeEnum.A_STRING
    else:
        c_type = None
    model.set_c_type(c_type)


def check_posix(model: SimpleDefinition) -> None:
    # pylint: disable=import-outside-toplevel
    from asn1_parser.asn1.validation.asn1_bundle_validator import (
        ASN1ConsistencyError,
    )

    name = model.get_type_name()
    posix = ASN1_POSIX_RANGE.get(name)
    if posix:
        begin = model.get_asn_type().get_begin()
        end = model.get_asn_type().get_end()
        if posix.get("begin") != begin or posix.get("end") != end:
            # pylint: disable=import-outside-toplevel

            raise ASN1ConsistencyError(
                f"Range [{begin} - {end}] doesn't match "
                f"with the used POSIX definition ({name})."
            )


def null_exception_catch(model: Union[KeyTypePair, SimpleDefinition]) -> None:
    if model.get_asn_type().get_type_name() == "NULL":
        # pylint: disable=import-outside-toplevel
        from asn1_parser.asn1.validation.asn1_bundle_validator import (
            ASN1ConsistencyError,
        )

        raise ASN1ConsistencyError(
            "Unexpected type: NULL. The NULL type is supported by"
            "the ASN.1 standard but its use is forbidden by the"
            "APG tool to avoid any confusion that could be caused"
            "by the presence of the NULL type in the generated C"
            "and COSMOS artifacts."
        )

    if isinstance(model, SimpleDefinition):
        check_posix(model)


def check_comment(model: Asn1Comment) -> None:
    assert isinstance(model, Asn1Comment), f"{model}"
    not_allowed = ["[", "]", "--"]
    for sign in not_allowed:
        if not model.get_comment():
            return
        if model.get_comment().find(sign) > -1:
            key = model.get_parent().get_key()
            comment = model.get_comment()
            raise TextXSyntaxError(
                f"Comment for '{key}' contains "
                f"an invalid sign '{sign}': '{comment}'"
            )


def check_enumerated(model: Enumerated) -> None:
    pos_sum = sum([e.get_pos() for e in model.get_enum()])
    if pos_sum == 0:
        # write position into object, when no positions are given
        pos = 0
        for enum in model.get_enum():
            enum.set_pos(pos)
            pos = pos + 1
    elif pos_sum != sum(i for i in range(len(model.get_enum()))):
        raise IndexError(
            "Some indices are not present, multiple times or out of bounds"
        )
    else:
        # if positions are given, sort the objects, checking that no position
        # is given multiple times
        ordered_enums: List[Any] = [None] * len(model.get_enum())
        for enum in model.get_enum():
            pos = enum.get_pos()
            if ordered_enums[pos] is None:
                ordered_enums[pos] = enum
            else:
                raise IndexError(f"index '{pos}' is defined multiple times")
        model.set_enum(ordered_enums)
