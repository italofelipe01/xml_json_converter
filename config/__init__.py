"""
Módulo config - Configurações do projeto
"""

from .settings import (
    DEFAULT_CONFIG,
    XML_TYPE_CONFIGS,
    CLI_CONFIG,
    get_config,
    ensure_directories
)

__all__ = [
    "DEFAULT_CONFIG",
    "XML_TYPE_CONFIGS", 
    "CLI_CONFIG",
    "get_config",
    "ensure_directories"
]