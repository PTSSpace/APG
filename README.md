# APG (ASN.1 Parser and Generator)

APG (ASN.1 Parser and Generator) is a tool that allows conversion of ASN.1
data files into a number of formats such as:

- [NASA core Flight System](https://github.com/nasa/cFS/) TM/TC C header files
- [COSMOS/OpenC3](https://github.com/OpenC3/cosmos) TM/TC text configuration files
- C structs
- Binary files

The most supported and most implemented use case: from the ASN.1 data definitions,
generate cFS and OpenC3 TM/TC definitions simultaneously and by doing this, have
the ASN.1 TM/TC database automatically synchronised between the embedded
software running NASA cFS and developer machine running COSMOS/OpenC3.

Note: The APN is early alpha quality and has not been used in any production
projects. Further development is still needed.

## Quick start

Install dependencies:

```bash
pip3 install -r requirements.txt
```

Run the tool:

```bash
python3 asn1_parser/main.py --help
```

Run the lints and tests:

```bash
invoke lint
invoke test
```

## Documentation

Documentation can be built and read by running:

```bash
pip3 install -r requirements.txt
invoke docs-all
```

## License

PTS license TBD.

## Copyright

Copyright (c) Planetary Transportation Systems GmbH 2022. 
