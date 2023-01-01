Introduction
============

This document contains the software-specific instructions for working with the
*ASN.1 Parser and Generator (APG)* tool.

The APG tool provides the following capabilities:

- Type-safe ASN.1 parser: read ASN.1 definitions defined in text files

- Build an ASN.1 in-memory representation of ASN.1 contents (ASN.1 Bundle data
  object)

- Validate the contents of the ASN.1 bundle

- Code and documentation generation: from in-memory ASN.1 bundle, produce
  several artifacts such as:

  - C data structs
  - COSMOS text files
  - Auto-generated Interface Control Document documentation

Applicable documents
====================

.. _ad1_ddjf:

* [AD1] KS-DF-1870000-X-0001-PTS - Design Definition and Justification File

.. _ad2_ttpu:

* [AD2] ECSS-E-ST-70-41C - Telemetry and telecommand packet utilization

.. _ad3_sdd:

* [AD3] KS-SDD-1870000-X-0001-PTS - Software Design Document

.. _ad4_srs:

* [AD4] KS-SRS-1870000-X-0001-PTS - Software Requirements Specification

.. _ad5_obcicd:

* [AD5] KS-ICD-1870000-X-0002-PTS - OBC Low-Level Flight Software Interface Control Document

Reference documents
===================

.. _rd1_itu_asn1:

* [RD1] Abstract Syntax Notation One (ASN.1): Specification of basic notation

  https://www.itu.int/ITU-T/studygroups/com17/languages/X.680-0207.pdf

.. _rd2_cosmos:

* [RD2] COSMOS v5 documentation

  https://cosmosc2.com/docs/v5/

.. _rd3_wiki_asn1:

* [RD3] Wikipedia - ASN.1

  https://en.wikipedia.org/wiki/ASN.1

Terms and abbreviations
=======================

.. list-table:: Terms and abbreviations
    :widths: 33 66

    * - **APG**
      - ASN.1 Parser and Generator (this tool)

    * - **APID**
      - Application Process Identifier (cf. CCSDS)

    * - **ASN.1**
      - Abstract Syntax Notation One

    * - **CCSDS**
      - Consultative Committee for Space Data Systems

    * - **COSMOS**
      - User interface for command and control of embedded systems

    * - **CRC**
      - Cyclic Redundancy Code

    * - **ECSS**
      - European Cooperation for Space Standardization

    * - **FSW**
      - Flight Software

    * - **PUS**
      - Packet Utilization Standard

    * - **TC**
      - Telecommand

    * - **TM**
      - Telemetry
