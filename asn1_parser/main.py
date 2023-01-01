#!/usr/bin/env python3

import os
import sys
from typing import Union

try:
    ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if not os.path.isdir(ROOT_PATH):
        raise FileNotFoundError
    sys.path.append(ROOT_PATH)
except FileNotFoundError:
    print("error: could not locate ASN.1 Parser's root folder.")
    sys.exit(1)

# pylint: disable=wrong-import-position

from asn1_parser.asn1.asn1_bundle import ASN1Bundle
from asn1_parser.asn1.asn1_bundle_builder import ASN1BundleBuilder
from asn1_parser.asn1.validation.asn1_bundle_validator import (
    ASN1ConsistencyError,
)
from asn1_parser.cli.cli_arg_parser import (
    GenerateBinaryCommandConfig,
    GenerateCCommandConfig,
    create_args_parser,
    GenerateCosmosCommandConfig,
    GenerateCFSCommandConfig,
)
from asn1_parser.generators.binary.generator import BinaryGenerator
from asn1_parser.generators.cfs.generator import CFSGenerator
from asn1_parser.generators.c.generator import CGenerator
from asn1_parser.generators.cosmos.generator import COSMOSGenerator


def main() -> None:
    parser = create_args_parser()
    config: Union[
        GenerateCosmosCommandConfig,
        GenerateCFSCommandConfig,
        GenerateCCommandConfig,
        GenerateBinaryCommandConfig,
    ]

    if parser.is_generate_cosmos_command():
        config = parser.get_generate_cosmos_config(ROOT_PATH)
        bundle: ASN1Bundle = ASN1BundleBuilder.build_from_cosmos_config(config)
        COSMOSGenerator.generate_cosmos(config, bundle)
    elif parser.is_generate_cfs_command():
        config = parser.get_generate_cfs_config(ROOT_PATH)
        try:
            bundle = ASN1BundleBuilder.build_from_cfs_config(config)
        except ASN1ConsistencyError as exception:
            print(
                f"error: an issue occurred when validating the ASN.1 bundle: "
                f"{exception.args[0]}."
            )
            sys.exit(1)
        CFSGenerator.generate_cfs(config, bundle)
    elif parser.is_generate_c_command():
        config = parser.get_generate_c_config(ROOT_PATH)
        try:
            bundle = ASN1BundleBuilder.build_from_c_config(config)
        except ASN1ConsistencyError as exception:
            print(
                f"error: an issue occurred when validating the ASN.1 bundle: "
                f"{exception.args[0]}."
            )
            sys.exit(1)
        CGenerator.generate_c(config, bundle)
    elif parser.is_generate_binary_command():
        config = parser.get_generate_binary_config(ROOT_PATH)
        try:
            bundle = ASN1BundleBuilder.build_from_binary_config(config)
        except ASN1ConsistencyError as exception:
            print(
                f"error: an issue occurred when validating the ASN.1 bundle: "
                f"{exception.args[0]}."
            )
            sys.exit(1)
        BinaryGenerator.generate_binary(config, bundle)
    else:
        raise NotImplementedError


if __name__ == "__main__":
    main()
