"""
XML to JSON Converter
Conversor profissional de XML para JSON com suporte específico para NFe brasileira
"""

__version__ = "1.0.0"
__author__ = "XML to JSON Converter Team"
__email__ = "dev@xmltojson.com"
__license__ = "MIT"
__description__ = (
    "Conversor profissional de XML para JSON com suporte específico para NFe brasileira"
)

# Imports principais para facilitar uso
from .core.converter import XMLToJSONConverter
from .models.nfe_extractor import NFEExtractor
from .utils.validators import XMLValidator
from .utils.formatters import XMLFormatter
from .utils.file_handler import FileHandler

# Lista de exports públicos
__all__ = [
    "XMLToJSONConverter",
    "NFEExtractor",
    "XMLValidator",
    "XMLFormatter",
    "FileHandler",
]

# Configuração de logging básica
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
