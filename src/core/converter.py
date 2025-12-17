"""
Módulo principal de conversão XML para JSON
"""

import logging
from pathlib import Path
from typing import Dict, Optional, Union
from collections import OrderedDict

from ..utils.file_handler import FileHandler
from ..utils.validators import XMLValidator
from ..utils.formatters import XMLFormatter
from .xml_parser import XMLParser

logger = logging.getLogger(__name__)


class XMLToJSONConverter:
    """
    Classe principal para conversão de XML para JSON
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa o conversor

        Args:
            config (dict, optional): Configurações personalizadas
        """
        self.config = config or {}
        self.file_handler = FileHandler()
        self.validator = XMLValidator()
        self.formatter = XMLFormatter()
        self.parser = XMLParser()

        # Configurações padrão
        self.default_settings = {
            "preserve_attributes": True,
            "clean_namespaces": True,
            "indent_json": 2,
            "ensure_ascii": False,
            "create_output_dir": True,
        }

    def convert_file(
        self,
        xml_path: Union[str, Path],
        json_path: Optional[Union[str, Path]] = None,
        **kwargs,
    ) -> Optional[Dict]:
        """
        Converte arquivo XML para JSON

        Args:
            xml_path: Caminho do arquivo XML
            json_path: Caminho do arquivo JSON de saída (opcional)
            **kwargs: Configurações adicionais

        Returns:
            Dict com os dados convertidos ou None em caso de erro
        """
        try:
            xml_path = Path(xml_path)

            # Valida se o arquivo existe
            if not self.file_handler.validate_file_exists(xml_path):
                logger.error(f"Arquivo não encontrado: {xml_path}")
                return None

            # Valida se é um arquivo XML válido
            if not self.validator.is_valid_xml_file(xml_path):
                logger.error(f"Arquivo XML inválido: {xml_path}")
                return None

            # Lê o arquivo XML
            xml_content = self.file_handler.read_file(xml_path)
            if xml_content is None:
                return None

            # Converte para JSON
            json_data = self.convert_string(xml_content, **kwargs)
            if json_data is None:
                return None

            # Salva em arquivo se especificado
            if json_path:
                json_path = Path(json_path)
                if self._save_json_file(json_data, json_path, **kwargs):
                    logger.info(f"Arquivo JSON salvo em: {json_path}")
                else:
                    logger.error(f"Erro ao salvar arquivo JSON: {json_path}")
                    return None

            return json_data

        except Exception as e:
            logger.exception(f"Erro na conversão: {e}")
            return None

    def convert_string(self, xml_string: str, **kwargs) -> Optional[Dict]:
        """
        Converte string XML para JSON

        Args:
            xml_string: String contendo XML
            **kwargs: Configurações adicionais

        Returns:
            Dict com os dados convertidos ou None em caso de erro
        """
        try:
            # Valida XML
            if not self.validator.is_valid_xml_string(xml_string):
                logger.error("XML inválido")
                return None

            # Faz parse do XML
            root = self.parser.parse_string(xml_string)
            if root is None:
                return None

            # Converte para dicionário
            settings = {**self.default_settings, **self.config, **kwargs}

            if settings.get("clean_namespaces", True):
                root_tag = self.formatter.clean_namespace(root.tag)
            else:
                root_tag = root.tag

            json_data = {root_tag: self.parser.element_to_dict(root, settings)}

            return json_data

        except Exception as e:
            logger.exception(f"Erro na conversão de string: {e}")
            return None

    def convert_batch(
        self,
        input_dir: Union[str, Path],
        output_dir: Optional[Union[str, Path]] = None,
        pattern: str = "*.xml",
        **kwargs,
    ) -> Dict[str, bool]:
        """
        Converte múltiplos arquivos XML em lote

        Args:
            input_dir: Diretório com arquivos XML
            output_dir: Diretório de saída (opcional)
            pattern: Padrão de arquivos (default: "*.xml")
            **kwargs: Configurações adicionais

        Returns:
            Dict com resultados {arquivo: sucesso}
        """
        input_dir = Path(input_dir)
        results = {}

        if not input_dir.exists():
            logger.error(f"Diretório não encontrado: {input_dir}")
            return results

        # Lista arquivos XML
        xml_files = list(input_dir.glob(pattern))

        if not xml_files:
            logger.warning(f"Nenhum arquivo XML encontrado em: {input_dir}")
            return results

        logger.info(f"Encontrados {len(xml_files)} arquivo(s) XML")

        # Define diretório de saída
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = input_dir / "converted"
            output_dir.mkdir(exist_ok=True)

        # Converte cada arquivo
        for xml_file in xml_files:
            json_file = output_dir / f"{xml_file.stem}.json"

            logger.info(f"Convertendo: {xml_file.name}")
            result = self.convert_file(xml_file, json_file, **kwargs)
            results[str(xml_file)] = result is not None

        success_count = sum(results.values())
        logger.info(f"Conversão concluída: {success_count}/{len(xml_files)} arquivos")

        return results

    def _save_json_file(self, data: Dict, json_path: Path, **kwargs) -> bool:
        """
        Salva dados JSON em arquivo

        Args:
            data: Dados para salvar
            json_path: Caminho do arquivo
            **kwargs: Configurações de formatação

        Returns:
            True se salvou com sucesso
        """
        try:
            settings = {**self.default_settings, **self.config, **kwargs}

            # Cria diretório se necessário
            if settings.get("create_output_dir", True):
                json_path.parent.mkdir(parents=True, exist_ok=True)

            # Configurações de formatação JSON
            json_kwargs = {
                "indent": settings.get("indent_json", 2),
                "ensure_ascii": settings.get("ensure_ascii", False),
                "separators": (",", ": "),
            }

            # Salva arquivo
            return self.file_handler.write_json_file(data, json_path, **json_kwargs)

        except Exception as e:
            logger.exception(f"Erro ao salvar JSON: {e}")
            return False

    def get_converter_stats(self) -> Dict:
        """
        Retorna estatísticas do conversor

        Returns:
            Dict com estatísticas
        """
        return {
            "config": self.config,
            "default_settings": self.default_settings,
            "validator": (
                self.validator.get_stats()
                if hasattr(self.validator, "get_stats")
                else {}
            ),
            "parser": (
                self.parser.get_stats() if hasattr(self.parser, "get_stats") else {}
            ),
        }
