# XML to JSON Converter

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow.svg?style=flat-square)
![Status](https://img.shields.io/badge/status-stable-success.svg?style=flat-square)
![CI](https://github.com/italofelipe01/xml_json_converter/actions/workflows/ci.yml/badge.svg)

> A professional, high-performance solution for converting XML files to JSON, with native and optimized support for Brazilian Electronic Invoices (NFe).

## 🎯 Product Overview

**XML to JSON Converter** is software designed to solve interoperability problems between legacy systems (XML-based) and modern architectures (JSON-based). The product stands out for its intelligent parsing capability for Brazilian fiscal documents, automatically extracting relevant metadata.

### ✨ Key Features

*   **Intelligent Bidirectional Conversion**: Transforms complex XML structures into clean, readable JSON objects.
*   **Fiscal Module (NFe)**: Specialized extractor for Invoices (NFe), identifying and formatting fields such as CNPJ, monetary values, and dates.
*   **Batch Processing**: Capability to process entire directories of files simultaneously.
*   **Robust CLI**: Complete command-line interface for integration with automation scripts.
*   **Schema Validation**: Verifies file integrity before conversion.

## 🛠️ Technologies Used

*   **Language**: Python 3.8+
*   **Core**: `xml.etree.ElementTree` (Built-in) for high performance without heavy dependencies.
*   **Engineering**: Modular structure (MVC), Unit Tests (`unittest`), Type Hinting, and PEP-8 compliance.

## 🚀 Installation and Usage

### Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/italofelipe01/xml_json_converter.git
cd xml_json_converter
pip install .
```

For development installation:

```bash
pip install -e .[dev]
```

### Usage Examples (CLI)

```bash
# Convert a single file
xml2json nota_fiscal.xml -o saida.json

# Convert entire directory and extract NFe data
xml2json -d ./entrada -o ./saida --nfe-info

# Show help
xml2json --help
```

Or using `python main.py`:

```bash
python main.py nota_fiscal.xml -o saida.json
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to report bugs, suggest features, or submit pull requests.

## 📄 License

This software is distributed under the **MIT** license. See the `LICENSE` file for more details.

## 👨‍💻 Authorship

Developed by **Ítalo Felipe Lira de Morais**.
