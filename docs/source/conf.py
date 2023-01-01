# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import string
import subprocess

# -- Get external input ------------------------------------------------------

GIT_HASH = (
    subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
    .decode("utf-8")
    .strip()
)
GIT_DATE = (
    subprocess.check_output(
        ["git", "show", "--no-patch", "--format=%cd", "--date=format:%d.%m.%Y"]
    )
    .decode("utf-8")
    .strip()
)

# -- Project information -----------------------------------------------------

project = "APG - Software User Manual"
copyright = "2021, Planetary Transportation Systems GmbH"
author = "Planetary Transportation Systems GmbH"


# Strings with embedded variables in Python
# https://stackoverflow.com/a/16553401/598057
class DocumentTemplate(string.Template):
    delimiter = "###"


DOCUMENT_NUMBER = "KS-UM-1870000-X-0003-PTS"
FSWF_VERSION = f"0.1 ({GIT_HASH})"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

latex_engine = "xelatex"

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = "_static/PTS_bow.png"

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
master_doc = "index"
latex_documents = [
    (master_doc, "APG-Software-User-Manual.tex", project, author, "book")
]

# - \usepackage[utf8x]{inputenc} enables UTF-8 support.
# - 'extraclassoptions': 'openany,oneside' removes second blank page.
# https://tex.stackexchange.com/a/327136/61966
latex_elements = {
    "extraclassoptions": "openany,oneside",
    # The paper size ('letterpaper' or 'a4paper').
    "papersize": "a4paper",
    # 'pointsize': '14pt', # this seems to have no effect
    "releasename": "",
    "geometry": r"""
\usepackage[
    top=1.5cm,
    bottom=1.5cm,
    left=1.5cm,
    right=1.5cm,
    headheight=50pt,
    includehead,
    includefoot,
    heightrounded,
]{geometry}
""",
    "sphinxsetup": "\
        verbatimwithframe=true, \
        VerbatimColor={rgb}{0.9,0.9,0.9}, \
        TitleColor={rgb}{0,0,0}, \
        InnerLinkColor={rgb}{0.1,0.1,0.1}, \
        OuterLinkColor={rgb}{1,0,0}",
    # Roboto is also a good choice.
    # sudo apt install fonts-roboto
    "fontpkg": r"""
\setmainfont{DejaVu Sans}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
    """,
    "tableofcontents": " ",
    "fncychap": "",
    "preamble": DocumentTemplate(
        r"""
        \usepackage{scrextend}
        \usepackage{makecell}
        \usepackage{colortbl}

        \definecolor{color_code}{rgb}{0.9, 0.9, 0.9}
        \definecolor{PTSHeaderGrayColor}{rgb}{.5,.5,.5}
        \definecolor{PTSHeaderLineGrayColor}{rgb}{.5,.5,.5}

        \setcounter{secnumdepth}{10}
        \setcounter{tocdepth}{10}

        \pagecolor [RGB]{255, 255, 255}

        % links

        \usepackage{hyperref}
        \hypersetup{
            colorlinks=true,
            linkcolor=[RGB]{35, 35, 35}, % color of internal links (change box color with linkbordercolor)
            citecolor=green,        % color of links to bibliography
            filecolor=magenta,      % color of file links
            urlcolor=cyan % This has an effect
        }

        % table

        \newcommand{\tablecell}[1] {{{#1}}}
        \protected\def\sphinxstyletheadfamily {\cellcolor{color_code}\bfseries}

        % inline code color

        \renewcommand{\sphinxcode}[1]{\colorbox{color_code}{#1}}

        % header

        \usepackage{fancyhdr}
        \usepackage{lastpage}
        % Save standard definitions
        \let\HeadRule\headrule
        \let\FootRule\footrule

        \renewcommand\headrule{\color{PTSHeaderLineGrayColor}\HeadRule}
        \renewcommand\footrule{\textcolor{PTSHeaderLineGrayColor}{\FootRule}}

        \makeatletter
            \newcommand\obctitlefont{\@setfontsize\Huge{28}{28}}
        \makeatother

        % "Since the first page of a chapter uses (by design) the plain style, you need to redefine this style:"
        % https://tex.stackexchange.com/a/157006/61966
        \fancypagestyle{plain}{
            \fancyhf{}
            \fancyhead[L]{
                \vspace*{0.05cm}{\includegraphics[scale=0.5]{PTS_bow.png}}
            }
            \fancyhead[C]{
                \textcolor{PTSHeaderGrayColor} {
                    \textnormal{\nouppercase{
                        ###DOCUMENT_NUMBER \\
                        ASN.1 Parser and Generator - Software User Manual \\
                    }}
                }
            }
            \fancyhead[R]{
                \textcolor{PTSHeaderGrayColor} { \footnotesize {
                    Issue: ###FSWF_VERSION \\
                    ###GIT_DATE \\
                    Page \textbf{\thepage} of \textbf{\pageref*{LastPage}} \\ \hspace*{-3mm}
                } }
            }
            \fancyfoot[C]{
                \textcolor{PTSHeaderGrayColor} {
                    © 2021 PTS GmbH
                }
                \\
                \vspace{1mm}
                \footnotesize { \textit { \textcolor{PTSHeaderGrayColor} {
                    This document is not to be reproduced, modified, adapted,
                    published, translated in any material form in whole or in part
                    without the prior written permission of
                    Planetary Transportation Systems GmbH
                    as the proprietor of this document.
                } } }
            }
            \renewcommand{\headrulewidth}{1.0pt}
            \renewcommand{\footrulewidth}{1.0pt}
        }

        \fancypagestyle{normal}{
            \fancyhf{}
            \fancyhead[L]{
                \vspace*{0.05cm}{\includegraphics[scale=0.5]{PTS_bow.png}}
            }
            \fancyhead[C]{
                \textcolor{PTSHeaderGrayColor} {
                    \textnormal{\nouppercase{
                        ###DOCUMENT_NUMBER \\
                        ASN.1 Parser and Generator - Software User Manual \\
                    }}
                }
            }
            \fancyhead[R]{
                \textcolor{PTSHeaderGrayColor} { \footnotesize {
                    Issue: ###FSWF_VERSION \\
                    ###GIT_DATE \\
                    Page \textbf{\thepage} of \textbf{\pageref*{LastPage}} \\ \hspace*{-3mm}
                } }
            }
            \fancyfoot[C]{
                \textcolor{PTSHeaderGrayColor} {
                    © 2021 PTS GmbH
                }
                \\
                \vspace{1mm}
                \footnotesize { \textit { \textcolor{PTSHeaderGrayColor} {
                    This document is not to be reproduced, modified, adapted,
                    published, translated in any material form in whole or in part
                    without the prior written permission of
                    Planetary Transportation Systems GmbH
                    as the proprietor of this document.
                } } }
            }
            \renewcommand{\headrulewidth}{1.0pt}
            \renewcommand{\footrulewidth}{1.0pt}
        }

        \usepackage{eqparbox}
        \usepackage{titletoc}
        \titlecontents{chapter}
                      [0em]
                      {\vspace{.25\baselineskip}}
                      {\raisebox{0.038cm}{\eqparbox{ch}{\thecontentslabel}\hspace{0.2cm}}}
                      {}
                      {\titlerule*[10pt]{$\cdot$}\contentspage}
        \titlecontents{section}
                      [0.5cm]
                      {\vspace{.25\baselineskip}}
                      {\raisebox{0.038cm}{\eqparbox{S}{\thecontentslabel}\hspace{0.2cm}}}
                      {}
                      {\titlerule*[10pt]{$\cdot$}\contentspage}
        \titlecontents{subsection}
                      [1cm]
                      {\vspace{.25\baselineskip}}
                      {\raisebox{0.038cm}{\eqparbox{Ss}{\thecontentslabel}\hspace{0.2cm}}}
                      {}
                      {\titlerule*[10pt]{$\cdot$}\contentspage}
        \titlecontents{subsubsection}
                      [1.5cm]
                      {\vspace{.25\baselineskip}}
                      {\raisebox{0.038cm}{\eqparbox{Sss}{\thecontentslabel}\hspace{0.2cm}}}
                      {}
                      {\titlerule*[10pt]{$\cdot$}\contentspage}
        \titlecontents{paragraph}
                      [2cm]
                      {\vspace{.25\baselineskip}}
                      {\raisebox{0.038cm}{\eqparbox{par}{\thecontentslabel}\hspace{0.2cm}}}
                      {}
                      {\titlerule*[10pt]{$\cdot$}\contentspage}
        \titlecontents{subparagraph}
                      [2.5cm]
                      {\vspace{.25\baselineskip}}
                      {\raisebox{0.038cm}{\eqparbox{subpar}{\thecontentslabel}\hspace{0.2cm}}}
                      {}
                      {\titlerule*[10pt]{$\cdot$}\contentspage}

        \titleformat{\chapter}[hang]
            {\normalfont\huge\bfseries}{\thechapter.}{3mm}{}
        \titlespacing*{\chapter}{0pt}{-24pt}{20pt}
    """
    ).substitute(
        FSWF_VERSION=FSWF_VERSION,
        DOCUMENT_NUMBER=DOCUMENT_NUMBER,
        GIT_DATE=GIT_DATE,
    ),
    "maketitle": DocumentTemplate(
        r"""
        % \pagenumbering{arabic}
        \begin{titlepage}
            \thispagestyle{plain}
            \vspace*{0mm} %%% * is used to give space from top

            \vspace{10mm}

            \begin{center}
                \obctitlefont{\textbf{ASN.1 Parser and Generator}} \\
                \obctitlefont{\textbf{Software User Manual}} \\
                \vspace{5mm}
                \LARGE{\textbf{###DOCUMENT_NUMBER}} \\

                \vspace{10mm}

                \includegraphics[scale=0.85]{PTS_bow.png}
            \end{center}

            \vspace{10mm}

            \begin{center}
                \bgroup
                    \def\arraystretch{1.5}%  1 is the default, change whatever you need
                    \begin{tabular}{|m{2.8cm}|m{5.0cm}|m{2.2cm}|m{4.4cm}|}
                    \hline
                        \cellcolor{gray!50}{\textbf{Function}} &
                        \cellcolor{gray!50}{\textbf{Name / Role}} &
                        \cellcolor{gray!50}{\textbf{Company}} &
                        \cellcolor{gray!50}{\textbf{Signature / Date}}
                    \\
                    \hline
                        \Gape[0.3cm][0cm]{\textbf{Created by}} &
                        Adrien Chardon, \newline
                        Software Engineer
                        &
                        PTS
                        &
                    \\
                    \hline
                        \Gape[0.3cm][0cm]{\textbf{Verified by}} &
                        Alexios Damigos, \newline
                        Software Engineer
                        &
                        PTS
                        &
                    \\
                    \hline
                        \Gape[0.3cm][0cm]{\textbf{Approved by}} &
                        Stanislav Pankevich, \newline
                        Software Development Lead
                        &
                        PTS
                        &
                    \\
                    \hline

                    \end{tabular}
                \egroup
            \end{center}

            \vspace{10mm}

            \begin{center}
                \bgroup
                    \def\arraystretch{1.5}%  1 is the default, change whatever you need
                    \begin{tabular}{|p{3.5cm}|p{8.4cm}|}
                    \hline
                    \cellcolor{gray!50}{\textbf{Document Ref.}} &
                    \makecell[l]{
                        ###DOCUMENT_NUMBER \\
                    }
                    \\ \hline
                    \cellcolor{gray!50}{\textbf{Version No.}} & \tablecell { ###FSWF_VERSION } \\ \hline
                    \cellcolor{gray!50}{\textbf{Date}} & \tablecell {###GIT_DATE} \\ \hline
                    \end{tabular}
                \egroup
            \end{center}

            \vspace{10mm}

            %% \vfill adds at the bottom
            %% \vfill
            \begin{addmargin}[1.05cm]{0cm}% left, right
                \textnormal {
                    \begin{center}
                        \textbf{Planetary Transportation Systems GmbH}\\
                        Plauener Str. 160B, 13053 Berlin, Germany\\
                        Internet: \url{www.pts.space} Mail: \href{mailto:info@pts.space}{info@pts.space}
                    \end{center}
                }
            \end{addmargin}
        \end{titlepage}

        %% \clearpage
        \pagestyle{normal}
        \setcounter{page}{2}
        \tableofcontents
        %% \listoffigures
        %% \listoftables
        \clearpage
        """
    ).substitute(
        FSWF_VERSION=FSWF_VERSION,
        DOCUMENT_NUMBER=DOCUMENT_NUMBER,
        GIT_DATE=GIT_DATE,
    ),
}

# https://www.sphinx-doc.org/en/master/_modules/sphinx/builders/linkcheck.html

# Don't block on broken or PTS internal links.
linkcheck_timeout = 10  # default: None
