import pytest

from textx.exceptions import TextXSyntaxError

from asn1_parser.asn1.grammar_elements.asn1_module import Asn1Module
from asn1_parser.asn1.parser import Asn1Parser


#####
# module
#####


@pytest.mark.skip(reason="TODO")
def test_module_comment_empty_line():
    input_asn = """
Module-test-module-comment-empty-line DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    -- test comment
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    # TODO


@pytest.mark.skip(reason="TODO")
def test_module_comment_empty_line_unit_only():
    input_asn = """
Module-test-module-comment-empty-line-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    -- [min]
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    # TODO


@pytest.mark.skip(reason="TODO")
def test_module_comment_empty_line_and_unit():
    input_asn = """
Module-test-module-comment-empty-line-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    -- [min] test comment
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    asn1_model: Asn1Module = Asn1Parser.parse_from_text(input_asn)
    assert isinstance(asn1_model, Asn1Module)

    # TODO


###


@pytest.mark.skip(reason="not implemented")
def test_module_end_comment():
    input_asn = """
Module-test-module-end-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END -- test comment
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError):
        Asn1Parser.parse_from_text(input_asn)


@pytest.mark.skip(reason="not implemented")
def test_module_end_comment_unit_only():
    input_asn = """
Module-test-module-end-comment-unit-only DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END -- [min]
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError):
        Asn1Parser.parse_from_text(input_asn)


@pytest.mark.skip(reason="not implemented")
def test_module_end_comment_and_unit():
    input_asn = """
Module-test-module-end-comment-and-unit DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED {
        carrot,
        apple
    }
END -- [min] test comment
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError):
        Asn1Parser.parse_from_text(input_asn)


#####
# incorrect comment
#####


def test_inline_comment():
    input_asn = """
Module-test-enumerated-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= -- test comment -- ENUMERATED {
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError):
        Asn1Parser.parse_from_text(input_asn)

    # TODO: This is very hard to maintain. Can we have a better way to check
    # this parsing error?
    # assert str(t_se.value) == (
    #   "None:2:16: error: Expected 'REAL' or 'INTEGER' or 'NULL' or 'BOOLEAN'"
    #   " or NameCapital at position (2, 16) => 'num-t ::= *-- test co'."
    # )


def _test_comment_unit_at_end():
    input_asn = """
Module-test-enumerated-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- test comment [min]
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError) as t_se:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        t_se.value.args[0].decode("utf-8") == "'[' is not allowed in a comment"
    )


def _test_comment_unit_between():
    input_asn = """
Module-test-enumerated-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- test [min] comment
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError) as t_se:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        t_se.value.args[0].decode("utf-8") == "'[' is not allowed in a comment"
    )


def _test_comment_open_brace_begin():
    input_asn = """
Module-test-enumerated-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- [ test comment
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError) as t_se:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        t_se.value.args[0].decode("utf-8") == "'[' is not allowed in a comment"
    )


def _test_comment_close_brace_begin():
    input_asn = """
Module-test-enumerated-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- ] test comment
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError) as t_se:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        t_se.value.args[0].decode("utf-8") == "']' is not allowed in a comment"
    )


def _test_comment_open_brace_middle():
    input_asn = """
Module-test-enumerated-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- test [ comment
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError) as t_se:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        t_se.value.args[0].decode("utf-8") == "'[' is not allowed in a comment"
    )


def _test_comment_close_brace_middle():
    input_asn = """
Module-test-enumerated-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- test ] comment
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError) as t_se:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        t_se.value.args[0].decode("utf-8") == "']' is not allowed in a comment"
    )


def _test_comment_open_brace_end():
    input_asn = """
Module-test-enumerated-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- test comment [
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError) as t_se:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        t_se.value.args[0].decode("utf-8") == "'[' is not allowed in a comment"
    )


def _test_comment_close_brace_end():
    input_asn = """
Module-test-enumerated-comment DEFINITIONS AUTOMATIC TAGS ::= BEGIN
    Enum-t ::= ENUMERATED { -- test comment ]
        carrot,
        apple
    }
END
""".lstrip()  # noqa: E501

    with pytest.raises(TextXSyntaxError) as t_se:
        Asn1Parser.parse_from_text(input_asn)

    assert (
        t_se.value.args[0].decode("utf-8") == "']' is not allowed in a comment"
    )
