"""
Setup script for XML to JSON Converter
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
project_root = Path(__file__).parent
readme_file = project_root / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = project_root / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() for line in f 
            if line.strip() and not line.startswith('#')
        ]
else:
    requirements = []

setup(
    name="xml-to-json-converter",
    version="1.0.0",
    author="XML to JSON Converter Team",
    author_email="dev@xmltojson.com",
    description="Conversor profissional de XML para JSON com suporte específico para NFe brasileira",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/xml-to-json-converter",
    project_urls={
        "Bug Tracker": "https://github.com/username/xml-to-json-converter/issues",
        "Documentation": "https://xml-to-json-converter.readthedocs.io/",
        "Source": "https://github.com/username/xml-to-json-converter",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "performance": [
            "ujson>=5.0.0",
            "lxml>=4.9.0",
        ],
        "validation": [
            "xmlschema>=2.0.0",
            "chardet>=5.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "xml2json=main:main",
            "xmltojson=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
        "src": ["*.py"],
        "config": ["*.py"],
        "examples": ["*.py", "*.xml", "*.json"],
        "docs": ["*.md", "*.rst"],
    },
    zip_safe=False,
    keywords=[
        "xml", "json", "converter", "nfe", "nota fiscal eletronica",
        "xml parser", "json generator", "brazilian nfe", "fiscal document",
        "data conversion", "file processing"
    ],
    platforms=["any"],
    license="MIT",
    
    # Metadata adicional
    maintainer="XML to JSON Converter Team",
    maintainer_email="dev@xmltojson.com",
    download_url="https://github.com/username/xml-to-json-converter/archive/v1.0.0.tar.gz",
    
    # Scripts adicionais
    scripts=[],
    
    # Configurações específicas
    options={
        "build_scripts": {
            "executable": "/usr/bin/env python3",
        },
    },
)