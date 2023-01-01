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


def test_module_begin_comment():
    input_asn = """
Module-test-module-begin-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN -- test comment
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    comment: Asn1Comment = asn1_model.get_comment()
    assert isinstance(comment, Asn1Comment)

    unit: str = comment.get_unit()
    assert unit == ""
    text: str = comment.get_comment()
    assert text == "test comment"


def test_module_begin_comment_unit_only():
    input_asn = """
Module-test-module-begin-comment-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN -- [min]
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    comment: Asn1Comment = asn1_model.get_comment()
    assert isinstance(comment, Asn1Comment)

    unit: str = comment.get_unit()
    assert unit == "min"
    text: str = comment.get_comment()
    assert text == ""


def test_module_begin_comment_and_unit():
    input_asn = """
Module-test-module-begin-comment-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN -- [min] test comment
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-enumerated-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- test comment
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-enumerated-item-comment-last-entry DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple -- test comment
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-enumerated-item-comment-entry DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot, -- test comment
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-enumerated-comment-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- [min]
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-enumerated-item-comment-last-entry-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple -- [min]
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-enumerated-item-comment-entry-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot, -- [min]
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-enumerated-comment-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- [min] test comment
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-enumerated-item-comment-last-entry-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple -- [min] test comment
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-enumerated-item-comment-entry-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot, -- [min] test comment
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-choice-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE { -- test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-choice-item-comment-last-entry DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- test comment
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-choice-item-comment-entry DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255), -- test comment
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-choice-comment-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE { -- [min]
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-choice-item-comment-last-entry-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min]
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-choice-item-comment-entry-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255), -- [min]
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-choice-comment-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE { -- [min] test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-choice-item-comment-last-entry-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min] test comment
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-choice-item-comment-entry-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Choice-t ::= CHOICE {
        carrot INTEGER(0..255), -- [min] test comment
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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


def test_sequence_comment():
    input_asn = """
Module-test-sequence-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE { -- test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definition: Sequence = asn1_model.get_definitions()[0]
    assert isinstance(definition, Sequence)

    comment: Asn1Comment = definition.get_comment()
    assert isinstance(comment, Asn1Comment)

    unit: str = comment.get_unit()
    assert unit == ""
    text: str = comment.get_comment()
    assert text == "test comment"


def test_sequence_item_comment_last_entry():
    input_asn = """
Module-test-sequence-comment-last-entry DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- test comment
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-sequence-comment-entry DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255), -- test comment
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    definition: Sequence = asn1_model.get_definitions()[0]
    assert isinstance(definition, Sequence)

    comment: Asn1Comment = definition.get_children()[0].get_comment()
    assert isinstance(comment, Asn1Comment)

    unit: str = comment.get_unit()
    assert unit == ""
    text: str = comment.get_comment()
    assert text == "test comment"


###


def test_sequence_comment_unit_only():
    input_asn = """
Module-test-sequence-comment-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE { -- [min]
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-sequence-comment-last-entry-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min]
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-sequence-comment-entry-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255), -- [min]
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-sequence-comment-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE { -- [min] test comment
        carrot INTEGER(0..255),
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-sequence-comment-last-entry-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255),
        apple INTEGER(0..255) -- [min] test comment
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-sequence-comment-entry-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Seq ::= SEQUENCE {
        carrot INTEGER(0..255), -- [min] test comment
        apple INTEGER(0..255)
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-simple-definition-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint16-t ::= INTEGER(0..65535) -- test comment
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-simple-definition-comment-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint16-t ::= INTEGER(0..65535) -- [min]
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
    input_asn = """
Module-test-simple-definition-comment-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Uint16-t ::= INTEGER(0..65535) -- [min] test comment
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
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
