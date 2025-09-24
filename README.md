# 🚀 Guia de Início Rápido - XML to JSON Converter

Este guia te ajudará a configurar e usar o projeto em poucos minutos.

## ⚡ Setup Rápido (2 minutos)

### 1. Clone e Configure
```bash
# Clone o repositório
git clone https://github.com/username/xml-to-json-converter.git
cd xml-to-json-converter

# Crie a estrutura de diretórios
mkdir -p src/core src/utils src/models src/cli config tests examples output logs
```

### 2. Crie os Arquivos
Copie o conteúdo dos artifacts para os seguintes arquivos:

```
xml_to_json_converter/
├── main.py                    # ← Artifact: main.py
├── src/
│   ├── __init__.py           # ← Artifact: init_files (primeira seção)
│   ├── core/
│   │   ├── __init__.py       # ← Artifact: init_files (segunda seção)
│   │   ├── converter.py      # ← Artifact: converter_py
│   │   └── xml_parser.py     # ← Artifact: xml_parser_py
│   ├── utils/
│   │   ├── __init__.py       # ← Artifact: init_files (terceira seção)
│   │   ├── file_handler.py   # ← Artifact: file_handler_py
│   │   ├── validators.py     # ← Artifact: validators_py
│   │   └── formatters.py     # ← Artifact: formatters_py
│   ├── models/
│   │   ├── __init__.py       # ← Artifact: init_files (quarta seção)
│   │   └── nfe_extractor.py  # ← Artifact: nfe_extractor_py
│   └── cli/
│       ├── __init__.py       # ← Artifact: init_files (quinta seção)
│       └── interface.py      # ← Artifact: cli_interface_py
├── config/
│   ├── __init__.py           # ← Artifact: init_files (sexta seção)
│   └── settings.py           # ← Artifact: settings_py
├── tests/
│   ├── __init__.py           # ← Artifact: init_files (sétima seção)
│   └── test_converter.py     # ← Artifact: test_converter_py
├── examples/
│   └── basic_usage.py        # ← Artifact: example_usage_py
├── requirements.txt          # ← Artifact: requirements_txt
├── setup.py                  # ← Artifact: setup_py
├── .gitignore               # ← Artifact: gitignore
├── Makefile                 # ← Artifact: makefile
└── README.md                # ← Artifact: readme_md
```

### 3. Teste Imediatamente
```bash
# Teste básico
python main.py --help

# Teste com seu arquivo XML (gas.xml que você forneceu)
python main.py gas.xml

# Teste com informações de NFe
python main.py gas.xml --nfe-info
```

## 🎯 Uso Básico (1 minuto)

### Conversão Simples
```bash
# Converte XML para JSON
python main.py seu_arquivo.xml

# Especifica arquivo de saída
python main.py seu_arquivo.xml -o saida_personalizada.json

# Conversão em lote (todo um diretório)
python main.py -d diretorio_com_xmls/ -r
```

### Uso Programático
```python
from src.core.converter import XMLToJSONConverter

# Cria conversor
converter = XMLToJSONConverter()

# Converte arquivo
resultado = converter.convert_file('arquivo.xml', 'saida.json')

# Converte string
xml_string = "<?xml version='1.0'?><root><item>valor</item></root>"
resultado = converter.convert_string(xml_string)
```

## 🇧🇷 Exemplo com NFe (30 segundos)

```python
from src.core.converter import XMLToJSONConverter
from src.models.nfe_extractor import NFEExtractor

# Converte NFe
converter = XMLToJSONConverter()
json_data = converter.convert_file('sua_nfe.xml')

# Extrai informações específicas da NFe
nfe_extractor = NFEExtractor()
info_nfe = nfe_extractor.extract_nfe_info(json_data)

# Mostra informações principais
print(f"NFe: {info_nfe['numero']}/{info_nfe['serie']}")
print(f"Emitente: {info_nfe['emitente_nome']}")
print(f"Valor: {info_nfe['valor_total']}")
```

## ⚙️ Configurações Rápidas

### Personalização Básica
```python
# Configuração personalizada
config = {
    'clean_namespaces': True,      # Remove namespaces
    'preserve_attributes': True,    # Mantém atributos XML
    'auto_type_conversion': True,   # Converte tipos (string → int, bool)
    'indent_json': 4               # Indentação do JSON
}

converter = XMLToJSONConverter(config=config)
```

### Via Linha de Comando
```bash
# Remove namespaces (padrão)
python main.py arquivo.xml

# Mantém namespaces
python main.py arquivo.xml --no-clean-namespaces

# JSON minimizado
python main.py arquivo.xml --minimize

# Mais detalhes
python main.py arquivo.xml --verbose
```

## 🧪 Testando (30 segundos)

```bash
# Testa se está funcionando
python -c "
from src.core.converter import XMLToJSONConverter
converter = XMLToJSONConverter()
xml = '<?xml version=\"1.0\"?><test><item>ok</item></test>'
result = converter.convert_string(xml)
print('✅ Funcionando!' if result else '❌ Erro!')
"

# Roda exemplo completo
python examples/basic_usage.py

# Roda testes unitários (opcional)
python -m pytest tests/ -v
```

## 🔧 Automação com Makefile

Se você tem `make` instalado:

```bash
# Setup completo
make setup

# Executa conversão
make run FILE=arquivo.xml

# Executa exemplos
make example

# Executa testes
make test

# Formata código
make format

# Ajuda completa
make help
```

## 📱 Exemplos Práticos

### 1. Conversão NFe Brasileira
```bash
# Converte NFe e mostra informações
python main.py nfe_exemplo.xml --nfe-info --verbose
```

### 2. Processamento em Lote
```bash
# Converte todos XMLs de uma pasta
python main.py -d pasta_com_nfes/ --pattern="*.xml" -r
```

### 3. Configurações Específicas
```bash
# Mantém namespaces e cria backup
python main.py arquivo.xml --no-clean-namespaces --backup
```

## 🚨 Resolução de Problemas

### Erro: "Módulo não encontrado"
```bash
# Certifique-se de estar no diretório do projeto
cd xml_to_json_converter

# Teste o path
python -c "import sys; print('\\n'.join(sys.path))"
```

### Erro: "Arquivo XML inválido"
```bash
# Valide o XML primeiro
python main.py arquivo.xml --validate-only
```

### Performance lenta
```bash
# Use configurações otimizadas
python main.py arquivo.xml --minimize --no-type-conversion
```

## 🎉 Pronto para Usar!

Agora você tem um conversor XML→JSON profissional funcionando! 

### Próximos Passos:
- 📚 Leia o [README.md](README.md) completo
- 🧪 Execute os [testes](tests/)
- 🔧 Explore as [configurações](config/settings.py)
- 💡 Veja mais [exemplos](examples/)

### Suporte:
- 📖 Documentação: `docs/`
- 🐛 Issues: GitHub Issues
- 💬 Discussões: GitHub Discussions

---
**⏱️ Tempo total de setup: ~3 minutos**

**🚀 Você agora pode converter XMLs para JSON como um profissional!**
│