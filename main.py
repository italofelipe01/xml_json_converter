"""
XML to JSON Converter
Ponto de entrada principal do projeto
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório src ao path para permitir imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from src.cli.interface import main as cli_main
from src.core.converter import XMLToJSONConverter
from config.settings import DEFAULT_CONFIG

def main():
    """Função principal do projeto"""
    try:
        # Inicia a interface CLI
        cli_main()
    except KeyboardInterrupt:
        print("\n\n👋 Operação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

def quick_convert(xml_path, json_path=None):
    """
    Função utilitária para conversão rápida via import
    
    Args:
        xml_path (str): Caminho do arquivo XML
        json_path (str, optional): Caminho do arquivo JSON de saída
    
    Returns:
        dict: Dados convertidos
    """
    converter = XMLToJSONConverter()
    return converter.convert_file(xml_path, json_path)

if __name__ == "__main__":
    main()