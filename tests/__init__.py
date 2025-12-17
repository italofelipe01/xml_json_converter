"""
Módulo tests - Testes automatizados
"""

# Configuração para testes
import sys
from pathlib import Path

# Adiciona src ao path para testes
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

__version__ = "1.0.0"
