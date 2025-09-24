#!/usr/bin/env python3
"""
Exemplo básico de uso do XML to JSON Converter
"""

import sys
from pathlib import Path

# Adiciona src ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from src.core.converter import XMLToJSONConverter
from src.models.nfe_extractor import NFEExtractor
from src.utils.formatters import XMLFormatter


def exemplo_basico():
    """Exemplo de conversão básica"""
    print("=" * 60)
    print("🔄 Exemplo Básico - XML to JSON Converter")
    print("=" * 60)
    
    # Cria instância do conversor
    converter = XMLToJSONConverter()
    
    # Arquivo XML de exemplo (substitua pelo seu arquivo)
    xml_file = "exemplo.xml"  # Coloque seu arquivo XML aqui
    json_file = "exemplo_convertido.json"
    
    # Verifica se arquivo existe
    if not Path(xml_file).exists():
        print(f"❌ Arquivo não encontrado: {xml_file}")
        print("💡 Coloque um arquivo XML no mesmo diretório deste exemplo")
        return
    
    print(f"📁 Convertendo: {xml_file}")
    
    # Converte arquivo
    result = converter.convert_file(xml_file, json_file)
    
    if result:
        print(f"✅ Conversão concluída: {json_file}")
        
        # Mostra algumas informações
        formatter = XMLFormatter()
        file_size = Path(json_file).stat().st_size
        print(f"📏 Tamanho do JSON: {formatter.get_size_formatted(file_size)}")
        
        # Se for NFe, extrai informações específicas
        if "nfe" in str(xml_file).lower():
            print("\n📋 Extraindo informações da NFe...")
            nfe_extractor = NFEExtractor()
            nfe_info = nfe_extractor.extract_nfe_info(result)
            
            if nfe_info:
                print("✅ Informações da NFe extraídas:")
                print(f"   • Número: {nfe_info.get('numero', 'N/A')}")
                print(f"   • Série: {nfe_info.get('serie', 'N/A')}")
                print(f"   • Emitente: {nfe_info.get('emitente_nome', 'N/A')}")
                print(f"   • Valor: {nfe_info.get('valor_total', 'N/A')}")
    else:
        print("❌ Erro na conversão")


def exemplo_string():
    """Exemplo de conversão de string XML"""
    print("\n" + "=" * 60)
    print("📝 Exemplo - Conversão de String XML")
    print("=" * 60)
    
    # XML de exemplo simples
    xml_string = """<?xml version="1.0" encoding="UTF-8"?>
    <pessoa>
        <nome>João Silva</nome>
        <idade>30</idade>
        <endereco>
            <rua>Rua das Flores, 123</rua>
            <cidade>São Paulo</cidade>
            <uf>SP</uf>
        </endereco>
        <telefones>
            <telefone tipo="celular">11999887766</telefone>
            <telefone tipo="fixo">1133334444</telefone>
        </telefones>
    </pessoa>"""
    
    converter = XMLToJSONConverter()
    
    print("🔄 Convertendo string XML...")
    result = converter.convert_string(xml_string)
    
    if result:
        print("✅ Conversão concluída!")
        
        # Mostra resultado formatado
        formatter = XMLFormatter()
        json_formatted = formatter.beautify_json(result)
        
        print("\n📄 Resultado JSON:")
        print(json_formatted)
    else:
        print("❌ Erro na conversão")


def exemplo_configuracao_personalizada():
    """Exemplo com configurações personalizadas"""
    print("\n" + "=" * 60)
    print("⚙️ Exemplo - Configurações Personalizadas")
    print("=" * 60)
    
    # Configurações personalizadas
    custom_config = {
        'clean_namespaces': False,  # Mantém namespaces
        'preserve_attributes': True,
        'auto_type_conversion': True,
        'indent_json': 4  # Indentação maior
    }
    
    # Cria conversor com configuração personalizada
    converter = XMLToJSONConverter(config=custom_config)
    
    # XML com namespace
    xml_with_namespace = """<?xml version="1.0" encoding="UTF-8"?>
    <root xmlns:nfe="http://example.com/nfe">
        <nfe:documento id="123">
            <nfe:titulo>Exemplo com Namespace</nfe:titulo>
            <nfe:valor>100.50</nfe:valor>
        </nfe:documento>
    </root>"""
    
    print("🔄 Convertendo com configurações personalizadas...")
    result = converter.convert_string(xml_with_namespace)
    
    if result:
        print("✅ Conversão concluída!")
        
        formatter = XMLFormatter()
        json_formatted = formatter.beautify_json(result, indent=4)
        
        print("\n📄 Resultado (namespaces preservados):")
        print(json_formatted)
    else:
        print("❌ Erro na conversão")


def exemplo_batch():
    """Exemplo de conversão em lote"""
    print("\n" + "=" * 60)
    print("📦 Exemplo - Conversão em Lote")
    print("=" * 60)
    
    # Diretório com XMLs (substitua pelo seu diretório)
    xml_directory = "xml_files"  # Crie este diretório e coloque XMLs
    
    if not Path(xml_directory).exists():
        print(f"❌ Diretório não encontrado: {xml_directory}")
        print("💡 Crie um diretório 'xml_files' e coloque alguns arquivos XML")
        return
    
    converter = XMLToJSONConverter()
    
    print(f"📁 Convertendo arquivos do diretório: {xml_directory}")
    
    # Conversão em lote
    results = converter.convert_batch(
        input_dir=xml_directory,
        output_dir="json_output",
        pattern="*.xml"
    )
    
    if results:
        success_count = sum(results.values())
        total_count = len(results)
        
        print(f"📊 Resultado:")
        print(f"   • Total: {total_count}")
        print(f"   • Sucessos: {success_count}")
        print(f"   • Falhas: {total_count - success_count}")
    else:
        print("❌ Nenhum arquivo foi processado")


def main():
    """Executa todos os exemplos"""
    try:
        exemplo_basico()
        exemplo_string()
        exemplo_configuracao_personalizada()
        exemplo_batch()
        
        print("\n" + "=" * 60)
        print("🎉 Exemplos concluídos!")
        print("=" * 60)
        print("💡 Para mais informações, consulte a documentação em docs/")
        
    except KeyboardInterrupt:
        print("\n\n👋 Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()