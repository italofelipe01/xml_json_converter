# XML to JSON Converter

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow.svg?style=flat-square)
![Status](https://img.shields.io/badge/status-stable-success.svg?style=flat-square)

> Uma solução profissional de alto desempenho para conversão de arquivos XML em JSON, com suporte nativo e otimizado para Nota Fiscal Eletrônica (NFe) brasileira.

## 🎯 Visão Geral do Produto

O **XML to JSON Converter** é um software desenvolvido para resolver problemas de interoperabilidade entre sistemas legados (baseados em XML) e arquiteturas modernas (baseadas em JSON). O produto se destaca pela capacidade de parsing inteligente de documentos fiscais brasileiros, extraindo metadados relevantes automaticamente.

### ✨ Principais Funcionalidades

* **Conversão Bidirecional Inteligente**: Transforma estruturas XML complexas em objetos JSON limpos e legíveis.
* **Módulo Fiscal (NFe)**: Extrator especializado para Notas Fiscais, identificando e formatando campos como CNPJ, valores monetários e datas.
* **Processamento em Lote**: Capacidade de processar diretórios inteiros de arquivos simultaneamente.
* **CLI Robusta**: Interface de linha de comando completa para integração com scripts de automação.
* **Validação de Schema**: Verifica a integridade dos arquivos antes da conversão.

## 🛠️ Tecnologias Utilizadas

* **Linguagem**: Python 3.8+
* **Core**: `xml.etree.ElementTree` (Built-in) para alta performance sem dependências pesadas.
* **Engenharia**: Estrutura modular (MVC), Testes Unitários (`unittest`), Type Hinting e aderência à PEP-8.

## 🚀 Instalação e Uso

### Instalação

```bash
git clone [https://github.com/italofelipe01/xml_json_converter.git](https://github.com/italofelipe01/xml_json_converter.git)
cd xml_json_converter
pip install -r requirements.txt
````

### Exemplo de Uso (CLI)

```bash
# Converter um arquivo único
python main.py nota_fiscal.xml -o saida.json

# Converter diretório inteiro e extrair dados de NFe
python main.py -d ./entrada -o ./saida --nfe-info
```

## 📄 Licença

Este software é distribuído sob a licença **MIT**. Consulte o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autoria

Desenvolvido por **Ítalo Felipe Lira de Morais**.
