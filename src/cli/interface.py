"""
Interface de linha de comando para o conversor XML to JSON
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from ..core.converter import XMLToJSONConverter
from ..models.nfe_extractor import NFEExtractor
from ..utils.formatters import XMLFormatter


def create_parser() -> argparse.ArgumentParser:
    """
    Cria parser de argumentos da linha de comando

    Returns:
        ArgumentParser configurado
    """
    parser = argparse.ArgumentParser(
        description="Converte arquivos XML para JSON",
        epilog="Exemplos de uso:\n"
        "  python main.py arquivo.xml\n"
        "  python main.py arquivo.xml -o saida.json\n"
        "  python main.py -d diretorio/ -r\n"
        "  python main.py arquivo.xml --nfe-info",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Argumentos principais
    parser.add_argument("input", nargs="?", help="Arquivo XML ou diretório de entrada")

    parser.add_argument(
        "-o",
        "--output",
        help="Arquivo JSON de saída (padrão: mesmo nome do XML com extensão .json)",
    )

    parser.add_argument(
        "-d", "--directory", help="Diretório com arquivos XML para conversão em lote"
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Busca recursiva em subdiretórios",
    )

    parser.add_argument(
        "--pattern",
        default="*.xml",
        help="Padrão de arquivos para busca (padrão: *.xml)",
    )

    # Configurações de conversão
    parser.add_argument(
        "--no-clean-namespaces",
        action="store_true",
        help="Não remove namespaces das tags",
    )

    parser.add_argument(
        "--no-attributes", action="store_true", help="Não preserva atributos XML"
    )

    parser.add_argument(
        "--no-type-conversion",
        action="store_true",
        help="Não converte tipos automaticamente",
    )

    parser.add_argument(
        "--indent", type=int, default=2, help="Indentação do JSON (padrão: 2)"
    )

    parser.add_argument(
        "--minimize", action="store_true", help="Gera JSON minimizado (sem indentação)"
    )

    # Funcionalidades específicas
    parser.add_argument(
        "--nfe-info", action="store_true", help="Extrai informações específicas de NFe"
    )

    parser.add_argument(
        "--validate-only", action="store_true", help="Apenas valida XML sem converter"
    )

    parser.add_argument(
        "--stats", action="store_true", help="Mostra estatísticas de conversão"
    )

    parser.add_argument(
        "--backup", action="store_true", help="Cria backup dos arquivos originais"
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Saída detalhada")

    parser.add_argument(
        "--version", action="version", version="XML to JSON Converter 1.0.0"
    )

    return parser


def print_header():
    """Imprime cabeçalho do programa"""
    print("=" * 60)
    print("🔄 XML to JSON Converter")
    print("=" * 60)


def print_file_info(file_path: Path, formatter: XMLFormatter):
    """
    Imprime informações do arquivo

    Args:
        file_path: Caminho do arquivo
        formatter: Instância do formatador
    """
    try:
        stat = file_path.stat()
        size_formatted = formatter.get_size_formatted(stat.st_size)

        print(f"📁 Arquivo: {file_path.name}")
        print(f"📏 Tamanho: {size_formatted}")
        print(f"📅 Modificado: {stat.st_mtime}")

    except Exception as e:
        print(f"❌ Erro ao obter informações do arquivo: {e}")


def handle_single_file(args, converter: XMLToJSONConverter):
    """
    Processa um único arquivo

    Args:
        args: Argumentos da linha de comando
        converter: Instância do conversor
    """
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"❌ Arquivo não encontrado: {input_path}")
        return False

    if args.verbose:
        print_file_info(input_path, XMLFormatter())

    # Define arquivo de saída
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".json")

    # Configurações de conversão
    conversion_settings = {
        "clean_namespaces": not args.no_clean_namespaces,
        "preserve_attributes": not args.no_attributes,
        "auto_type_conversion": not args.no_type_conversion,
        "indent_json": 0 if args.minimize else args.indent,
    }

    # Apenas validação
    if args.validate_only:
        print("🔍 Validando XML...")
        is_valid = converter.validator.is_valid_xml_file(input_path)
        if is_valid:
            print("✅ XML válido!")
        else:
            print("❌ XML inválido!")
            errors = converter.validator.get_last_errors(3)
            for error in errors:
                print(f"   • {error}")
        return is_valid

    # Conversão
    print(f"🔄 Convertendo: {input_path.name}")

    if args.backup:
        converter.file_handler.backup_file(input_path)

    result = converter.convert_file(input_path, output_path, **conversion_settings)

    if result:
        print(f"✅ Conversão concluída: {output_path}")

        # Informações específicas de NFe
        if args.nfe_info:
            nfe_extractor = NFEExtractor()
            nfe_data = nfe_extractor.extract_nfe_info(result)
            if nfe_data:
                print("\n📋 Informações da NFe:")
                for key, value in nfe_data.items():
                    print(f"   • {key}: {value}")

        # Estatísticas
        if args.stats:
            stats = converter.get_converter_stats()
        print("\n📊 Estatísticas:")
        val_count = stats.get("validator", {}).get("validations_performed", 0)
        print(f"   • Validações: {val_count}")
        parse_count = stats.get("parser", {}).get("parsed_elements", 0)
        print(f"   • Elementos processados: {parse_count}")

        return True
    else:
        print(f"❌ Erro na conversão de {input_path.name}")
        return False


def handle_directory(args, converter: XMLToJSONConverter):
    """
    Processa diretório com múltiplos arquivos

    Args:
        args: Argumentos da linha de comando
        converter: Instância do conversor
    """
    input_dir = Path(args.directory)

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"❌ Diretório não encontrado: {input_dir}")
        return False

    print(f"📁 Processando diretório: {input_dir}")

    # Configurações de conversão
    conversion_settings = {
        "clean_namespaces": not args.no_clean_namespaces,
        "preserve_attributes": not args.no_attributes,
        "auto_type_conversion": not args.no_type_conversion,
        "indent_json": 0 if args.minimize else args.indent,
    }

    # Conversão em lote
    results = converter.convert_batch(
        input_dir, pattern=args.pattern, **conversion_settings
    )

    # Relatório
    success_count = sum(results.values())
    total_count = len(results)

    print(f"\n📊 Relatório da conversão:")
    print(f"   • Total de arquivos: {total_count}")
    print(f"   • Conversões bem-sucedidas: {success_count}")
    print(f"   • Falhas: {total_count - success_count}")

    if args.verbose and results:
        print(f"\n📄 Detalhes:")
        for file_path, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {Path(file_path).name}")

    # Estatísticas gerais
    if args.stats:
        stats = converter.get_converter_stats()
        print("\n📈 Estatísticas gerais:")
        val_count = stats.get("validator", {}).get("validations_performed", 0)
        print(f"   • Validações: {val_count}")
        parse_count = stats.get("parser", {}).get("parsed_elements", 0)
        print(f"   • Elementos processados: {parse_count}")
        error_count = stats.get("validator", {}).get("invalid_files", 0)
        print(f"   • Erros de validação: {error_count}")

    return success_count > 0


def main():
    """Função principal da interface CLI"""
    parser = create_parser()

    # Se não há argumentos, mostra help
    if len(sys.argv) == 1:
        print_header()
        parser.print_help()
        print("\n💡 Dica: Use 'python main.py arquivo.xml' para conversão simples")
        return

    args = parser.parse_args()

    # Verifica se foi fornecido input ou diretório
    if not args.input and not args.directory:
        print("❌ Erro: Especifique um arquivo XML ou use --directory")
        parser.print_help()
        return

    print_header()

    # Cria instância do conversor
    converter = XMLToJSONConverter()

    try:
        # Processamento por diretório
        if args.directory:
            success = handle_directory(args, converter)
        # Processamento de arquivo único
        else:
            success = handle_single_file(args, converter)

        if success:
            print(f"\n🎉 Operação concluída com sucesso!")
        else:
            print(f"\n❌ Operação falhou!")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n\n👋 Operação cancelada pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
