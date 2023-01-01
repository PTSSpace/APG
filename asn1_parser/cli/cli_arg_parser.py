import argparse
from typing import List, Optional


def _parse_comma_separated_string_argument(fields: str) -> List[str]:
    fields_array = fields.split(",")
    return fields_array


def cli_args_parser() -> argparse.ArgumentParser:
    # How to parse multiple nested sub-commands using python argparse?
    # https://stackoverflow.com/a/19476216/598057
    main_parser = argparse.ArgumentParser()

    command_subparsers = main_parser.add_subparsers(
        title="command", dest="command"
    )
    command_subparsers.required = True

    # Generate COSMOS commands
    command_parser_generate_cosmos = command_subparsers.add_parser(
        "generate-cosmos",
        help="Generate COSMOS artefacts.",
        parents=[],
        description=(
            "Generate command: "
            "input ASN.1 files are generated into COSMOS files."
        ),
    )
    command_parser_generate_cosmos.add_argument(
        "input_paths",
        type=str,
        nargs="+",
        help="One or more folders with *.asn files",
    )
    command_parser_generate_cosmos.add_argument(
        "--asn1-module",
        type=str,
        help="ASN.1 module to generate.",
        required=True,
    )
    command_parser_generate_cosmos.add_argument(
        "--asn1-messages",
        type=_parse_comma_separated_string_argument,
        help="ASN.1 messages to generate.",
        required=True,
    )
    command_parser_generate_cosmos.add_argument(
        "--output-file-name",
        type=str,
        help="Output COSMOS file name.",
        required=True,
    )
    command_parser_generate_cosmos.add_argument(
        "--output-dir",
        type=str,
        help="Output folder",
        default="output/cosmos",
    )

    # Generate cFS commands
    command_parser_generate_cfs = command_subparsers.add_parser(
        "generate-cfs",
        help="Generate cFS artefacts.",
        parents=[],
        description=(
            "Generate command: input ASN.1 files are generated into cFS files."
        ),
    )
    command_parser_generate_cfs.add_argument(
        "input_paths",
        type=str,
        nargs="+",
        help="One or more folders with *.asn files",
    )
    command_parser_generate_cfs.add_argument(
        "--asn1-modules",
        type=_parse_comma_separated_string_argument,
        help="ASN.1 modules to generate.",
        required=True,
    )
    command_parser_generate_cfs.add_argument(
        "--output-dir",
        type=str,
        help="Output folder",
        default="output/cfs",
    )

    # Generate C commands
    command_parser_generate_c = command_subparsers.add_parser(
        "generate-c",
        help="Generate C artefacts.",
        parents=[],
        description=(
            "Generate command: input ASN.1 files are generated into C files."
        ),
    )
    command_parser_generate_c.add_argument(
        "input_paths",
        type=str,
        nargs="+",
        help="One or more folders with *.asn files",
    )
    command_parser_generate_c.add_argument(
        "--asn1-modules",
        type=_parse_comma_separated_string_argument,
        help="ASN.1 modules to generate.",
        required=True,
    )
    command_parser_generate_c.add_argument(
        "--output-dir",
        type=str,
        help="Output folder",
        default="output/c",
    )

    # Generate binary commands
    command_parser_generate_binary = command_subparsers.add_parser(
        "generate-binary",
        help="Generate C artefacts.",
        parents=[],
        description=(
            "Generate command: input ASN.1 files are generated into binary "
            "files."
        ),
    )
    command_parser_generate_binary.add_argument(
        "input_paths",
        type=str,
        nargs="+",
        help="One or more folders with *.asn files",
    )
    command_parser_generate_binary.add_argument(
        "--asn1-modules",
        type=_parse_comma_separated_string_argument,
        help="ASN.1 modules to generate.",
        required=True,
    )
    command_parser_generate_binary.add_argument(
        "--output-dir",
        type=str,
        help="Output folder",
        default="output/binary",
    )

    command_parser_generate_binary.add_argument(
        "--endianness",
        choices=["little-endian", "big-endian"],
        help="Endianness of the binary representation.",
    )

    return main_parser


class GenerateCosmosCommandConfig:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        project_root_path: str,
        input_paths: List[str],
        asn1_module: str,
        asn1_messages: List[str],
        output_file_name: str,
        output_dir: str,
    ) -> None:
        self.project_root_path = project_root_path
        self.input_paths = input_paths
        self.asn1_modules = [asn1_module]
        self.asn1_messages = asn1_messages
        self.output_file_name = output_file_name
        self.output_dir = output_dir


class GenerateCFSCommandConfig:
    def __init__(
        self,
        project_root_path: str,
        input_paths: List[str],
        asn1_modules: List[str],
        output_dir: str,
    ) -> None:
        self.project_root_path = project_root_path
        self.input_paths = input_paths
        self.asn1_modules = asn1_modules
        self.output_dir = output_dir


class GenerateCCommandConfig:
    def __init__(
        self,
        project_root_path: str,
        input_paths: List[str],
        asn1_modules: List[str],
        output_dir: str,
    ) -> None:
        self.project_root_path = project_root_path
        self.input_paths = input_paths
        self.asn1_modules = asn1_modules
        self.output_dir = output_dir


class GenerateBinaryCommandConfig:
    def __init__(
        self,
        project_root_path: str,
        input_paths: List[str],
        asn1_modules: List[str],
        output_dir: str,
        endianness: str,
    ) -> None:  # pylint: disable=too-many-arguments
        self.project_root_path = project_root_path
        self.input_paths = input_paths
        self.asn1_modules = asn1_modules
        self.output_dir = output_dir
        self.endianness = endianness


class ASN1ArgsParser:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args

    def is_generate_cosmos_command(self) -> bool:
        return bool(self.args.command == "generate-cosmos")

    def get_generate_cosmos_config(
        self, project_root_path: str
    ) -> GenerateCosmosCommandConfig:
        return GenerateCosmosCommandConfig(
            project_root_path,
            self.args.input_paths,
            self.args.asn1_module,
            self.args.asn1_messages,
            self.args.output_file_name,
            self.args.output_dir,
        )

    def is_generate_cfs_command(self) -> bool:
        return bool(self.args.command == "generate-cfs")

    def get_generate_cfs_config(
        self, project_root_path: str
    ) -> GenerateCFSCommandConfig:
        return GenerateCFSCommandConfig(
            project_root_path,
            self.args.input_paths,
            self.args.asn1_modules,
            self.args.output_dir,
        )

    def is_generate_c_command(self) -> bool:
        return bool(self.args.command == "generate-c")

    def get_generate_c_config(
        self, project_root_path: str
    ) -> GenerateCCommandConfig:
        return GenerateCCommandConfig(
            project_root_path,
            self.args.input_paths,
            self.args.asn1_modules,
            self.args.output_dir,
        )

    def is_generate_binary_command(self) -> bool:
        return bool(self.args.command == "generate-binary")

    def get_generate_binary_config(
        self, project_root_path: str
    ) -> GenerateBinaryCommandConfig:
        return GenerateBinaryCommandConfig(
            project_root_path,
            self.args.input_paths,
            self.args.asn1_modules,
            self.args.output_dir,
            self.args.endianness,
        )


def create_args_parser(
    testing_args: Optional[argparse.Namespace] = None,
) -> ASN1ArgsParser:
    args = testing_args
    if not args:
        parser = cli_args_parser()
        args = parser.parse_args()
    return ASN1ArgsParser(args)
