from typing import List

from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.grammar_elements.asn1_comment import Asn1Comment
from asn1_parser.asn1.grammar_elements.choice import Choice
from asn1_parser.asn1.grammar_elements.enumerated import Enumerated
from asn1_parser.asn1.grammar_elements.sequence import Sequence
from asn1_parser.asn1.grammar_elements.simple_definition import SimpleDefinition
from asn1_parser.asn1.parser import Asn1Parser

#####
# module
#####

# pylint: disable=line-too-long
# line-too-long warning shows up for the asn modules only
# only other way to disable would be concatenating multiple strings
# to form the modules, but that degrades readability


def test_module_begin_comment():
    input_asn = [
        """
Module-test-module-begin-comment-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN -- test comment
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-module-begin-comment-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN -- test comment
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        comment: Asn1Comment = asn1_model.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


def test_module_begin_comment_unit_only():
    input_asn = [
        """
Module-test-module-begin-comment-unit-only-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN -- [min]
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-module-begin-comment-unit-only-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN -- [min]
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        comment: Asn1Comment = asn1_model.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


def test_module_begin_comment_and_unit():
    input_asn = [
        """
Module-test-module-begin-comment-and-unit-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN -- [min] test comment
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-module-begin-comment-and-unit-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN -- [min] test comment
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        comment: Asn1Comment = asn1_model.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


#####
# enumerated
#####


def test_enumerated_comment():
    input_asn = [
        """
Module-test-enumerated-comment-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- test comment
        carrot,
        apple
    }
END
""".lstrip(),
        """
Module-test-enumerated-comment-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- test comment
        carrot,
        apple
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Enumerated = asn1_model.get_definitions()[0]
        assert isinstance(definition, Enumerated)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


def test_enumerated_item_comment_last_entry():
    input_asn = [
        """
Module-test-enumerated-item-comment-last-entry-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple -- test comment
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-enumerated-item-comment-last-entry-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple -- test comment
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Enumerated = asn1_model.get_definitions()[0]
        assert isinstance(definition, Enumerated)

        comment: Asn1Comment = definition.get_enum()[1].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


def test_enumerated_item_comment_entry():
    input_asn = [
        """
Module-test-enumerated-item-comment-entry-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot, -- test comment
        apple
    }
END
""".lstrip(),
        """
Module-test-enumerated-item-comment-entry-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot, -- test comment
        apple
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Enumerated = asn1_model.get_definitions()[0]
        assert isinstance(definition, Enumerated)

        comment: Asn1Comment = definition.get_enum()[0].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


###


def test_enumerated_comment_unit_only():
    input_asn = [
        """
Module-test-enumerated-comment-unit-only-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- [min]
        carrot,
        apple
    }
END
""".lstrip(),
        """
Module-test-enumerated-comment-unit-only-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- [min]
        carrot,
        apple
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Enumerated = asn1_model.get_definitions()[0]
        assert isinstance(definition, Enumerated)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


def test_enumerated_item_comment_last_entry_unit_only():
    input_asn = [
        """
Module-test-enumerated-item-comment-last-entry-unit-only-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple -- [min]
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-enumerated-item-comment-last-entry-unit-only-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple -- [min]
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Enumerated = asn1_model.get_definitions()[0]
        assert isinstance(definition, Enumerated)

        comment: Asn1Comment = definition.get_enum()[1].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


def test_enumerated_item_comment_entry_unit_only():
    input_asn = [
        """
Module-test-enumerated-item-comment-entry-unit-only-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot, -- [min]
        apple
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-enumerated-item-comment-entry-unit-only-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot, -- [min]
        apple
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Enumerated = asn1_model.get_definitions()[0]
        assert isinstance(definition, Enumerated)

        comment: Asn1Comment = definition.get_enum()[0].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


###


def test_enumerated_comment_and_unit():
    input_asn = [
        """
Module-test-enumerated-comment-and-unit-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- [min] test comment
        carrot,
        apple
    }
END
""".lstrip(),
        """
Module-test-enumerated-comment-and-unit-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- [min] test comment
        carrot,
        apple
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Enumerated = asn1_model.get_definitions()[0]
        assert isinstance(definition, Enumerated)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


def test_enumerated_item_comment_last_entry_and_unit():
    input_asn = [
        """
Module-test-enumerated-item-comment-last-entry-and-unit-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple -- [min] test comment
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-enumerated-item-comment-last-entry-and-unit-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple -- [min] test comment
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Enumerated = asn1_model.get_definitions()[0]
        assert isinstance(definition, Enumerated)

        comment: Asn1Comment = definition.get_enum()[1].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


def test_enumerated_item_comment_entry_and_unit():
    input_asn = [
        """
Module-test-enumerated-item-comment-entry-and-unit-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot, -- [min] test comment
        apple
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-enumerated-item-comment-entry-and-unit-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot, -- [min] test comment
        apple
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Enumerated = asn1_model.get_definitions()[0]
        assert isinstance(definition, Enumerated)

        comment: Asn1Comment = definition.get_enum()[0].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


#####
# choice
#####


def test_choice_comment():
    input_asn = [
        """
Module-test-choice-comment-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE { -- test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
        """
Module-test-choice-comment-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE { -- test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Choice = asn1_model.get_definitions()[0]
        assert isinstance(definition, Choice)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


def test_choice_item_comment_last_entry():
    input_asn = [
        """
Module-test-choice-item-comment-last-entry-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- test comment
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-choice-item-comment-last-entry-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- test comment
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Choice = asn1_model.get_definitions()[0]
        assert isinstance(definition, Choice)

        comment: Asn1Comment = definition.get_children()[1].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


def test_choice_item_comment_entry():
    input_asn = [
        """
Module-test-choice-item-comment-entry-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255), -- test comment
        apple INTEGER(0..255)
    }
END
""".lstrip(),
        """
Module-test-choice-item-comment-entry-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255), -- test comment
        apple INTEGER(0..255)
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Choice = asn1_model.get_definitions()[0]
        assert isinstance(definition, Choice)

        comment: Asn1Comment = definition.get_children()[0].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


###


def test_choice_comment_unit_only():
    input_asn = [
        """
Module-test-choice-comment-unit-only-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE { -- [min]
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
        """
Module-test-choice-comment-unit-only-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE { -- [min]
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Choice = asn1_model.get_definitions()[0]
        assert isinstance(definition, Choice)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


def test_choice_item_comment_last_entry_unit_only():
    input_asn = [
        """
Module-test-choice-item-comment-last-entry-unit-only-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min]
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-choice-item-comment-last-entry-unit-only-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min]
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Choice = asn1_model.get_definitions()[0]
        assert isinstance(definition, Choice)

        comment: Asn1Comment = definition.get_children()[1].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


def test_choice_item_comment_entry_unit_only():
    input_asn = [
        """
Module-test-choice-item-comment-entry-unit-only-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255), -- [min]
        apple INTEGER(0..255)
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-choice-item-comment-entry-unit-only-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255), -- [min]
        apple INTEGER(0..255)
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Choice = asn1_model.get_definitions()[0]
        assert isinstance(definition, Choice)

        comment: Asn1Comment = definition.get_children()[0].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


###


def test_choice_comment_and_unit():
    input_asn = [
        """
Module-test-choice-comment-and-unit-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE { -- [min] test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
        """
Module-test-choice-comment-and-unit-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE { -- [min] test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Choice = asn1_model.get_definitions()[0]
        assert isinstance(definition, Choice)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


def test_choice_item_comment_last_entry_and_unit():
    input_asn = [
        """
Module-test-choice-item-comment-last-entry-and-unit-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min] test comment
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-choice-item-comment-last-entry-and-unit-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min] test comment
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Choice = asn1_model.get_definitions()[0]
        assert isinstance(definition, Choice)

        comment: Asn1Comment = definition.get_children()[1].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


def test_choice_item_comment_entry_and_unit():
    input_asn = [
        """
Module-test-choice-item-comment-entry-and-unit-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255), -- [min] test comment
        apple INTEGER(0..255)
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-choice-item-comment-entry-and-unit-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255), -- [min] test comment
        apple INTEGER(0..255)
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Choice = asn1_model.get_definitions()[0]
        assert isinstance(definition, Choice)

        comment: Asn1Comment = definition.get_children()[0].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


#####
# sequence
#####


def test_sequence_comment_simple():
    input_asn = [
        """
Module-test-sequence-comment-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE { -- test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
        """
Module-test-sequence-comment-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE { -- test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


def test_sequence_comment_spaces():
    def _gen_asn_and_basic_asserts(input_asn):
        asn1_model = Asn1Parser.parse_from_text(input_asn)
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        return definition

    #
    # Simple comment with spaces
    #

    expected_comment, input_asn = (
        "seq test comment",
        """
            Module-test-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
                Seq ::= SEQUENCE {            --              seq test comment
                    carrot INTEGER(0..255),
                    apple INTEGER(0..255)
                }
            END
        """,
    )

    definition = _gen_asn_and_basic_asserts(input_asn)
    assert isinstance(definition, Sequence)

    comment: Asn1Comment = definition.get_comment()
    assert isinstance(comment, Asn1Comment)
    assert comment.get_comment() == expected_comment
    assert comment.get_unit() == ""

    #
    # Comment with spaces and unit
    #

    expected_comment, input_asn = (
        "seq test comment",
        """
            Module-test-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
                Seq ::= SEQUENCE {            -- [unit]             seq test comment
                    carrot INTEGER(0..255),
                    apple INTEGER(0..255)
                }
            END
        """,  # noqa: E501
    )

    definition = _gen_asn_and_basic_asserts(input_asn)
    assert isinstance(definition, Sequence)

    comment: Asn1Comment = definition.get_comment()
    assert isinstance(comment, Asn1Comment)
    assert comment.get_comment() == expected_comment
    assert comment.get_unit() == "unit"


def test_sequence_item_comment_last_entry():
    input_asn = [
        """
Module-test-sequence-comment-last-entry-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- test comment
    }
END
""".lstrip(),
        """
Module-test-sequence-comment-last-entry-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- test comment
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        comment: Asn1Comment = definition.get_children()[1].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


def test_sequence_item_comment_entry():
    input_asn = [
        """
Module-test-sequence-comment-entry-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255), -- test comment
        apple INTEGER(0..255)
    }
END
""".lstrip(),
        """
Module-test-sequence-comment-entry-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255), -- test comment
        apple INTEGER(0..255)
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        comment: Asn1Comment = definition.get_children()[0].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


def test_sequence_comment_misc_characters():
    def _gen_asn_and_basic_asserts(input_asn):
        asn1_model = Asn1Parser.parse_from_text(input_asn)
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        return definition

    #
    # Seq
    #

    expected_comment, input_asn = (
        "seq test comment with _ and - and ( and !",
        """
            Module-test-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
                Seq ::= SEQUENCE { -- seq test comment with _ and - and ( and !
                    carrot INTEGER(0..255),
                    apple INTEGER(0..255)
                }
            END
        """,  # noqa: E501
    )

    definition = _gen_asn_and_basic_asserts(input_asn)
    assert isinstance(definition, Sequence)

    comment: Asn1Comment = definition.get_comment()
    assert isinstance(comment, Asn1Comment)
    assert comment.get_comment() == expected_comment
    assert comment.get_unit() == ""

    #
    # Item 1
    #

    expected_comment, input_asn = (
        "carrot test comment with _ and - and ( and !",
        """
            Module-test-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
                Seq ::= SEQUENCE {
                    carrot INTEGER(0..255), -- carrot test comment with _ and - and ( and !
                    apple INTEGER(0..255)
                }
            END
        """,  # noqa: E501
    )

    definition = _gen_asn_and_basic_asserts(input_asn)
    assert isinstance(definition, Sequence)

    sequence = definition.get_children()
    comment: Asn1Comment = sequence[0].get_comment()
    assert isinstance(comment, Asn1Comment)
    assert comment.get_comment() == expected_comment
    assert comment.get_unit() == ""

    #
    # Item 2
    #

    expected_comment, input_asn = (
        "apple test comment with _ and - and ( and !",
        """
            Module-test-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
                Seq ::= SEQUENCE {
                    carrot INTEGER(0..255),
                    apple INTEGER(0..255) -- apple test comment with _ and - and ( and !
                }
            END
        """,  # noqa: E501
    )

    definition = _gen_asn_and_basic_asserts(input_asn)
    assert isinstance(definition, Sequence)

    sequence = definition.get_children()
    comment: Asn1Comment = sequence[1].get_comment()
    assert isinstance(comment, Asn1Comment)
    assert comment.get_comment() == expected_comment
    assert comment.get_unit() == ""


def test_first_item_comment():
    def _gen_asn_and_basic_asserts(input_asn):
        asn1_model = Asn1Parser.parse_from_text(input_asn)
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        return definition

    #
    # Simple comment with spaces
    #

    expected_comment, input_asn = (
        "first item test comment",
        """
            Module-test-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
                Seq ::= SEQUENCE {
                    carrot INTEGER(0..255),             --              first item test comment
                    apple INTEGER(0..255)
                }
            END
        """,  # noqa: E501
    )

    definition = _gen_asn_and_basic_asserts(input_asn)
    assert isinstance(definition, Sequence)

    sequence = definition.get_children()
    comment: Asn1Comment = sequence[0].get_comment()
    assert isinstance(comment, Asn1Comment)
    assert comment.get_comment() == expected_comment
    assert comment.get_unit() == ""

    #
    # Comment with spaces and unit
    #

    expected_comment, input_asn = (
        "first item test comment",
        """
            Module-test-sequence DEFINITIONS AUTOMATIC TAGS ::= BEGIN
                Seq ::= SEQUENCE {
                    carrot INTEGER(0..255),             -- [unit]             first item test comment
                    apple INTEGER(0..255)
                }
            END
        """,  # noqa: E501
    )

    definition = _gen_asn_and_basic_asserts(input_asn)
    assert isinstance(definition, Sequence)

    sequence = definition.get_children()
    comment: Asn1Comment = sequence[0].get_comment()
    assert isinstance(comment, Asn1Comment)
    assert comment.get_comment() == expected_comment
    assert comment.get_unit() == "unit"


def test_last_item_comment():
    def _gen_asn_and_basic_asserts(input_asn):
        asn1_model = Asn1Parser.parse_from_text(input_asn)
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        return definition

    #
    # Simple comment with spaces
    #

    expected_comment, input_asn = (
        "last item test comment",
        """
            Module-test-sequence-comment-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
                Seq ::= SEQUENCE {
                    carrot INTEGER(0..255),
                    apple INTEGER(0..255)               --              last item test comment
                }
            END
        """,  # noqa: E501
    )

    definition = _gen_asn_and_basic_asserts(input_asn)
    assert isinstance(definition, Sequence)

    sequence = definition.get_children()
    comment: Asn1Comment = sequence[1].get_comment()
    assert isinstance(comment, Asn1Comment)
    assert comment.get_comment() == expected_comment
    assert comment.get_unit() == ""

    #
    # Comment with spaces and unit
    #

    expected_comment, input_asn = (
        "last item test comment",
        """
            Module-test-sequence-comment-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
                Seq ::= SEQUENCE {
                    carrot INTEGER(0..255),
                    apple INTEGER(0..255)               -- [unit]             last item test comment
                }
            END
        """,  # noqa: E501
    )

    definition = _gen_asn_and_basic_asserts(input_asn)
    assert isinstance(definition, Sequence)

    sequence = definition.get_children()
    comment: Asn1Comment = sequence[1].get_comment()
    assert isinstance(comment, Asn1Comment)
    assert comment.get_comment() == expected_comment
    assert comment.get_unit() == "unit"


###


def test_sequence_comment_unit_only():
    input_asn = [
        """
Module-test-sequence-comment-unit-only-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE { -- [min]
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
        """
Module-test-sequence-comment-unit-only-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE { -- [min]
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


def test_sequence_item_comment_last_entry_unit_only():
    input_asn = [
        """
Module-test-sequence-comment-last-entry-unit-only-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min]
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-sequence-comment-last-entry-unit-only-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min]
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        comment: Asn1Comment = definition.get_children()[1].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


def test_sequence_item_comment_entry_unit_only():
    input_asn = [
        """
Module-test-sequence-comment-entry-unit-only-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255), -- [min]
        apple INTEGER(0..255)
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-sequence-comment-entry-unit-only-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255), -- [min]
        apple INTEGER(0..255)
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        comment: Asn1Comment = definition.get_children()[0].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


###


def test_sequence_comment_and_unit():
    input_asn = [
        """
Module-test-sequence-comment-and-unit-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE { -- [min] test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
        """
Module-test-sequence-comment-and-unit-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE { -- [min] test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


def test_sequence_item_comment_last_entry_and_unit():
    input_asn = [
        """
Module-test-sequence-comment-last-entry-and-unit-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min] test comment
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-sequence-comment-last-entry-and-unit-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min] test comment
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        comment: Asn1Comment = definition.get_children()[1].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


def test_sequence_item_comment_entry_and_unit():
    input_asn = [
        """
Module-test-sequence-comment-entry-and-unit-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255), -- [min] test comment
        apple INTEGER(0..255)
    }
END
""".lstrip(),  # noqa: E501
        """
Module-test-sequence-comment-entry-and-unit-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255), -- [min] test comment
        apple INTEGER(0..255)
    }
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: Sequence = asn1_model.get_definitions()[0]
        assert isinstance(definition, Sequence)

        comment: Asn1Comment = definition.get_children()[0].get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


#####
# sequence WITH COMPONENT
#####

# TODO

#####
# definition
#####


def test_simple_definition_comment():
    input_asn = [
        """
Module-test-simple-definition-comment-1 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint16-t ::= INTEGER(0..65535) -- test comment
END
""".lstrip(),
        """
Module-test-simple-definition-comment-2 DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint16-t ::= INTEGER(0..65535) -- test comment
END
""".lstrip(),
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: SimpleDefinition = asn1_model.get_definitions()[0]
        assert isinstance(definition, SimpleDefinition)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == ""
        text: str = comment.get_comment()
        assert text == "test comment"


###


def test_simple_definition_comment_unit_only():
    input_asn = [
        """
Module-test-simple-definition-comment-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint16-t ::= INTEGER(0..65535) -- [min]
END
""".lstrip(),  # noqa: E501
        """
Module-test-simple-definition-comment-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint16-t ::= INTEGER(0..65535) -- [min]
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: SimpleDefinition = asn1_model.get_definitions()[0]
        assert isinstance(definition, SimpleDefinition)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == ""


###


def test_simple_definition_comment_and_unit():
    input_asn = [
        """
Module-test-simple-definition-comment-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint16-t ::= INTEGER(0..65535) -- [min] test comment
END
""".lstrip(),  # noqa: E501
        """
Module-test-simple-definition-comment-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint16-t ::= INTEGER(0..65535) -- [min] test comment
END
""".lstrip(),  # noqa: E501
    ]

    asn1_models: List[Asn1Module] = Asn1Parser.parse_from_text_multimodule(
        input_asn
    )
    for asn1_model in asn1_models:
        assert isinstance(asn1_model, Asn1Module)

        definition: SimpleDefinition = asn1_model.get_definitions()[0]
        assert isinstance(definition, SimpleDefinition)

        comment: Asn1Comment = definition.get_comment()
        assert isinstance(comment, Asn1Comment)

        unit: str = comment.get_unit()
        assert unit == "min"
        text: str = comment.get_comment()
        assert text == "test comment"


#####
# different kinds of units
#####

# TODO
