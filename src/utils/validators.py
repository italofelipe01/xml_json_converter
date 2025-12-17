"""
Módulo de validações
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union, Dict, List, Optional
import re


class XMLValidator:
    """
    Classe para validações XML
    """

    def __init__(self):
        """Inicializa validador"""
        self.stats = {
            "validations_performed": 0,
            "valid_files": 0,
            "invalid_files": 0,
            "validation_errors": [],
        }

    def is_valid_xml_string(self, xml_string: str) -> bool:
        """
        Valida se string é XML válido

        Args:
            xml_string: String para validar

        Returns:
            True se XML é válido
        """
        self.stats["validations_performed"] += 1

        try:
            ET.fromstring(xml_string)
            self.stats["valid_files"] += 1
            return True
        except ET.ParseError as e:
            self.stats["invalid_files"] += 1
            self.stats["validation_errors"].append(str(e))
            return False
        except Exception as e:
            self.stats["invalid_files"] += 1
            self.stats["validation_errors"].append(f"Erro inesperado: {str(e)}")
            return False

    def is_valid_xml_file(self, file_path: Union[str, Path]) -> bool:
        """
        Valida se arquivo é XML válido

        Args:
            file_path: Caminho do arquivo

        Returns:
            True se arquivo XML é válido
        """
        self.stats["validations_performed"] += 1

        try:
            path = Path(file_path)

            # Verifica se arquivo existe
            if not path.exists():
                error_msg = f"Arquivo não encontrado: {file_path}"
                self.stats["validation_errors"].append(error_msg)
                self.stats["invalid_files"] += 1
                return False

            # Verifica extensão
            if not self.has_xml_extension(path):
                error_msg = f"Arquivo não tem extensão XML: {file_path}"
                self.stats["validation_errors"].append(error_msg)
                self.stats["invalid_files"] += 1
                return False

            # Tenta fazer parse do arquivo
            ET.parse(str(path))
            self.stats["valid_files"] += 1
            return True

        except ET.ParseError as e:
            error_msg = f"XML inválido em {file_path}: {str(e)}"
            self.stats["validation_errors"].append(error_msg)
            self.stats["invalid_files"] += 1
            return False
        except Exception as e:
            error_msg = f"Erro ao validar {file_path}: {str(e)}"
            self.stats["validation_errors"].append(error_msg)
            self.stats["invalid_files"] += 1
            return False

    def has_xml_extension(self, file_path: Union[str, Path]) -> bool:
        """
        Verifica se arquivo tem extensão XML

        Args:
            file_path: Caminho do arquivo

        Returns:
            True se tem extensão XML
        """
        xml_extensions = [".xml", ".nfe", ".cte", ".mdfe"]
        return Path(file_path).suffix.lower() in xml_extensions

    def check_xml_encoding(self, file_path: Union[str, Path]) -> Optional[str]:
        """
        Detecta encoding do arquivo XML

        Args:
            file_path: Caminho do arquivo

        Returns:
            Encoding detectado ou None
        """
        try:
            with open(file_path, "rb") as file:
                # Lê primeiros bytes para detectar encoding
                first_bytes = file.read(100)

            # Converte para string tentando UTF-8
            try:
                header = first_bytes.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    header = first_bytes.decode("latin-1")
                except UnicodeDecodeError:
                    return None

            # Procura declaração de encoding
            encoding_match = re.search(
                r'encoding=["\']([^"\']+)["\']', header, re.IGNORECASE
            )
            if encoding_match:
                return encoding_match.group(1).lower()

            # Default para UTF-8 se não encontrar
            return "utf-8"

        except Exception:
            return None

    def validate_xml_structure(
        self, xml_string: str, required_elements: List[str] = None
    ) -> Dict:
        """
        Valida estrutura específica do XML

        Args:
            xml_string: String XML
            required_elements: Lista de elementos obrigatórios

        Returns:
            Dict com resultado da validação
        """
        result = {
            "valid": False,
            "root_element": None,
            "namespace": None,
            "required_elements_found": [],
            "missing_elements": [],
            "total_elements": 0,
            "attributes_count": 0,
        }

        try:
            root = ET.fromstring(xml_string)
            result["root_element"] = self._clean_namespace(root.tag)
            result["valid"] = True

            # Extrai namespace
            if "}" in root.tag:
                result["namespace"] = root.tag.split("}")[0][1:]

            # Conta elementos e atributos
            result["total_elements"] = len(list(root.iter()))
            result["attributes_count"] = sum(len(elem.attrib) for elem in root.iter())

            # Verifica elementos obrigatórios
            if required_elements:
                found_elements = [
                    self._clean_namespace(elem.tag) for elem in root.iter()
                ]
                result["required_elements_found"] = [
                    elem for elem in required_elements if elem in found_elements
                ]
                result["missing_elements"] = [
                    elem for elem in required_elements if elem not in found_elements
                ]

        except ET.ParseError as e:
            result["error"] = str(e)

        return result

    def validate_nfe_structure(self, xml_string: str) -> Dict:
        """
        Validação específica para NFe brasileira

        Args:
            xml_string: String XML da NFe

        Returns:
            Dict com resultado da validação NFe
        """
        nfe_required_elements = [
            "nfeProc",
            "NFe",
            "infNFe",
            "ide",
            "emit",
            "dest",
            "det",
            "total",
            "transp",
            "pag",
            "protNFe",
        ]

        result = self.validate_xml_structure(xml_string, nfe_required_elements)

        # Validações específicas da NFe
        try:
            root = ET.fromstring(xml_string)

            # Verifica se é realmente uma NFe
            root_tag = self._clean_namespace(root.tag)
            result["is_nfe"] = root_tag in ["nfeProc", "NFe"]

            # Verifica namespace da NFe
            expected_namespace = "http://www.portalfiscal.inf.br/nfe"
            result["correct_namespace"] = expected_namespace in xml_string

            # Verifica chave da NFe
            nfe_element = root.find(".//{http://www.portalfiscal.inf.br/nfe}infNFe")
            if nfe_element is not None:
                nfe_id = nfe_element.get("Id", "")
                result["has_nfe_key"] = nfe_id.startswith("NFe") and len(nfe_id) == 47
                result["nfe_key"] = nfe_id
            else:
                result["has_nfe_key"] = False
                result["nfe_key"] = None

        except Exception as e:
            result["nfe_validation_error"] = str(e)

        return result

    def validate_file_size(
        self, file_path: Union[str, Path], max_size_mb: float = 50.0
    ) -> bool:
        """
        Valida tamanho do arquivo

        Args:
            file_path: Caminho do arquivo
            max_size_mb: Tamanho máximo em MB

        Returns:
            True se arquivo está dentro do limite
        """
        try:
            size_bytes = Path(file_path).stat().st_size
            size_mb = size_bytes / (1024 * 1024)

            if size_mb > max_size_mb:
                error_msg = (
                    f"Arquivo muito grande: {size_mb:.2f}MB (máximo: {max_size_mb}MB)"
                )
                self.stats["validation_errors"].append(error_msg)
                return False

            return True

        except Exception as e:
            error_msg = f"Erro ao verificar tamanho do arquivo: {str(e)}"
            self.stats["validation_errors"].append(error_msg)
            return False

    def _clean_namespace(self, tag: str) -> str:
        """
        Remove namespace do nome da tag

        Args:
            tag: Nome da tag com namespace

        Returns:
            Nome da tag sem namespace
        """
        return re.sub(r"\{.*\}", "", tag)

    def get_stats(self) -> Dict:
        """
        Retorna estatísticas de validação

        Returns:
            Dict com estatísticas
        """
        return self.stats.copy()

    def reset_stats(self):
        """Reset das estatísticas"""
        self.stats = {
            "validations_performed": 0,
            "valid_files": 0,
            "invalid_files": 0,
            "validation_errors": [],
        }

    def get_last_errors(self, count: int = 5) -> List[str]:
        """
        Retorna últimos erros de validação

        Args:
            count: Número de erros para retornar

        Returns:
            Lista com últimos erros
        """
        return (
            self.stats["validation_errors"][-count:]
            if self.stats["validation_errors"]
            else []
        )
