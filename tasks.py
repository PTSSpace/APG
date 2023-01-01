import os
import re

import invoke
from invoke import task


# Please also modify .pylint.ini:256
LINE_LENGTH = 80


def oneline_command(string):
    return re.sub("\\s+", " ", string).strip()


def run_invoke_cmd(context, cmd):
    return context.run(
        cmd, env=None, hide=False, warn=False, pty=False, echo=True
    )


@task
def clean(context):
    find_command = oneline_command(
        """
        find
            tests/integration
            -type f \\(
                -name '*.script'
            \\)
            -or -type d \\(
                -name '*.dSYM' -or
                -name 'Sandbox' -or
                -name 'Output' -or
                -name 'output'
            \\)
            -not -path "**Expected**"
            -not -path "**Input**"
        """
    )

    find_result = run_invoke_cmd(context, find_command)
    find_result_stdout = find_result.stdout.strip()
    echo_command = oneline_command(f"echo {find_result_stdout} | xargs rm -rfv")

    run_invoke_cmd(context, echo_command)


@task
def docs_lint(context):
    """
    Run the linters on the docs.

    For now, only the Sphinx's linkcheck tool is run.

    `CURL_CA_BUNDLE=""` is a dirty hack used to disable SSL verification.
    Ref: https://stackoverflow.com/q/48391750
    """
    run_invoke_cmd(
        context,
        oneline_command(
            """
        cd docs &&
            make linkcheck
    """
        ),
    )


@task
def docs_sphinx(context):
    """
    Generate the Software User Manual from Sphinx .rst (via .tex) to .pdf.
    """
    run_invoke_cmd(
        context,
        oneline_command(
            """
        cd docs &&
          SPHINXOPTS="-W --keep-going -n" make html latexpdf
    """
        ),
    )


@task
def docs_see(context):
    """
    Open the Software User Manual.
    """
    run_invoke_cmd(
        context,
        oneline_command(
            """
        cd docs &&
          see "build/latex/APG-Software-User-Manual.pdf"
    """
        ),
    )


@task(docs_lint, docs_sphinx, docs_see)
def docs_all(context):  # pylint: disable=unused-argument
    pass


@task
def test_unit(context, focus=None):
    filter_or_empty = f"-k {focus}" if focus else ""

    command = oneline_command(
        f"""
        pytest --capture=no {filter_or_empty}
        """
    )

    run_invoke_cmd(context, command)


@task(clean)
def test_integration(context, focus=None, debug=False):
    cwd = os.getcwd()

    asn1_parser_exec = f'python3 \\"{cwd}/asn1_parser/main.py\\"'

    focus_or_none = f"--filter {focus}" if focus else ""
    debug_opts = "-vv --show-all" if debug else ""

    command = oneline_command(
        """
        lit
        --param ASN1_PARSER_EXEC="{asn1_parser_exec}"
        -v
        {debug_opts}
        {focus_or_none}
        {cwd}/tests/integration
        """
    ).format(
        asn1_parser_exec=asn1_parser_exec,
        cwd=cwd,
        debug_opts=debug_opts,
        focus_or_none=focus_or_none,
    )

    run_invoke_cmd(context, command)


@task
def lint_black_diff(context):
    command = oneline_command(
        f"""
        black . --line-length {LINE_LENGTH} --color 2>&1
        """
    )
    result = run_invoke_cmd(context, command)

    # black always exits with 0, so we handle the output.
    if "reformatted" in result.stdout:
        print("invoke: black found issues")
        result.exited = 1
        raise invoke.exceptions.UnexpectedExit(result)


@task
def lint_pylint(context):
    command = oneline_command(
        """
        pylint --rcfile=.pylint.ini asn1_parser/ tests/unit/ tasks.py
        """
    )
    try:
        run_invoke_cmd(context, command)
    except invoke.exceptions.UnexpectedExit as exc:
        # pylint doesn't show an error message when exit code != 0, so we do.
        print(f"invoke: pylint exited with error code {exc.result.exited}")
        raise exc


@task
def lint_flake8(context):
    command = oneline_command(
        f"""
        flake8 .
            --exclude=.venv,docs
            --statistics
            --max-line-length {LINE_LENGTH}
            --show-source
        """
    )
    run_invoke_cmd(context, command)


@task
def lint_mypy(context):
    command = oneline_command(
        """
        mypy asn1_parser/
            --show-error-codes
            --disable-error-code=import
            --enable-error-code=misc
            --strict
        """
    )
    run_invoke_cmd(context, command)


@task(lint_black_diff, lint_pylint, lint_flake8, lint_mypy)
def lint(_):
    pass


@task(test_unit, test_integration)
def test(_):
    pass


@task(lint, test)
def check(_):
    pass
