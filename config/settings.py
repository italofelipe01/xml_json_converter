"""
Configurações do projeto XML to JSON Converter
"""

import os
from pathlib import Path

# Diretórios do projeto
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
OUTPUT_DIR = PROJECT_ROOT / "output"
EXAMPLES_DIR = PROJECT_ROOT / "examples"
TESTS_DIR = PROJECT_ROOT / "tests"
DOCS_DIR = PROJECT_ROOT / "docs"

# Configurações padrão do conversor
DEFAULT_CONFIG = {
    # Configurações XML
    'clean_namespaces': True,
    'preserve_attributes': True,
    'auto_type_conversion': True,
    'preserve_order': True,
    
    # Configurações JSON
    'indent_json': 2,
    'ensure_ascii': False,
    'sort_keys': False,
    'separators': (',', ': '),
    
    # Configurações de arquivo
    'create_output_dir': True,
    'backup_original': False,
    'overwrite_existing': True,
    
    # Configurações de validação
    'validate_before_convert': True,
    'max_file_size_mb': 50.0,
    'supported_encodings': ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252'],
    
    # Configurações de limpeza
    'remove_empty_strings': False,
    'remove_none_values': False,
    'remove_empty_dicts': False,
    'remove_empty_lists': False,
    
    # Configurações específicas NFe
    'extract_nfe_info': True,
    'format_nfe_values': True,
    'validate_nfe_structure': True
}

# Extensões de arquivo suportadas
SUPPORTED_XML_EXTENSIONS = ['.xml', '.nfe', '.cte', '.mdfe']
OUTPUT_JSON_EXTENSION = '.json'

# Padrões de arquivo para busca
DEFAULT_XML_PATTERNS = [
    '*.xml',
    '*.nfe',
    '*.cte',
    '*.mdfe'
]

# Configurações de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': PROJECT_ROOT / 'logs' / 'converter.log',
    'max_log_size_mb': 10,
    'backup_count': 5
}

# Configurações de performance
PERFORMANCE_CONFIG = {
    'batch_size': 100,
    'memory_limit_mb': 500,
    'timeout_seconds': 300,
    'max_concurrent_files': 4
}

# Configurações específicas por tipo de XML
XML_TYPE_CONFIGS = {
    'nfe': {
        'required_elements': [
            'nfeProc', 'NFe', 'infNFe', 'ide', 'emit', 'dest'
        ],
        'namespace': 'http://www.portalfiscal.inf.br/nfe',
        'version_attribute': 'versao',
        'extract_specific_info': True
    },
    'cte': {
        'required_elements': [
            'cteProc', 'CTe', 'infCte', 'ide', 'emit', 'dest'
        ],
        'namespace': 'http://www.portalfiscal.inf.br/cte',
        'version_attribute': 'versao',
        'extract_specific_info': False
    },
    'mdfe': {
        'required_elements': [
            'mdfeProc', 'MDFe', 'infMDFe', 'ide', 'emit'
        ],
        'namespace': 'http://www.portalfiscal.inf.br/mdfe',
        'version_attribute': 'versao',
        'extract_specific_info': False
    },
    'generic': {
        'required_elements': [],
        'namespace': None,
        'version_attribute': None,
        'extract_specific_info': False
    }
}

# Configurações de interface CLI
CLI_CONFIG = {
    'show_progress': True,
    'use_colors': True,
    'verbose_default': False,
    'confirm_overwrite': True,
    'show_file_info': True
}

# Mensagens de erro comuns
ERROR_MESSAGES = {
    'file_not_found': "Arquivo não encontrado: {file_path}",
    'invalid_xml': "XML inválido: {error}",
    'conversion_failed': "Falha na conversão: {error}",
    'permission_denied': "Permissão negada: {file_path}",
    'disk_space': "Espaço em disco insuficiente",
    'memory_limit': "Limite de memória excedido",
    'timeout': "Operação expirou após {timeout} segundos"
}

# Configurações de desenvolvimento
DEV_CONFIG = {
    'debug_mode': os.getenv('DEBUG', 'False').lower() == 'true',
    'profiling_enabled': False,
    'test_data_dir': TESTS_DIR / 'sample_data',
    'generate_test_files': False
}

# Configurações de produção
PROD_CONFIG = {
    'optimize_memory': True,
    'enable_caching': False,
    'max_workers': 4,
    'error_reporting': True
}

# Função para obter configuração baseada no ambiente
def get_config():
    """
    Retorna configuração baseada no ambiente
    
    Returns:
        Dict com configurações
    """
    config = DEFAULT_CONFIG.copy()
    
    # Aplica configurações específicas do ambiente
    if DEV_CONFIG['debug_mode']:
        config.update({
            'indent_json': 4,
            'validate_before_convert': True,
            'backup_original': True
        })
    else:
        config.update(PROD_CONFIG)
        
    return config

# Função para criar diretórios necessários
def ensure_directories():
    """Cria diretórios necessários do projeto"""
    directories = [
        OUTPUT_DIR,
        PROJECT_ROOT / 'logs',
        TESTS_DIR / 'sample_data'
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Executa setup inicial
if __name__ == "__main__":
    ensure_directories()
    print(f"✅ Diretórios do projeto criados")
    print(f"📁 Projeto: {PROJECT_ROOT}")
    print(f"📁 Saída: {OUTPUT_DIR}")
    print(f"📁 Testes: {TESTS_DIR}")
    print(f"🔧 Debug: {DEV_CONFIG['debug_mode']}")