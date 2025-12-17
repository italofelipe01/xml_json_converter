"""
Módulo de formatação e limpeza de dados
"""

import re
from typing import Dict, Any, Optional, Union
from datetime import datetime
import json


class XMLFormatter:
    """
    Classe para formatação e limpeza de dados XML
    """

    def __init__(self):
        """Inicializa formatador"""
        self.namespace_pattern = re.compile(r"\{.*\}")
        self.date_patterns = [
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[-+]\d{2}:\d{2}",  # ISO 8601 com timezone
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",  # ISO 8601 sem timezone
            r"\d{4}-\d{2}-\d{2}",  # Data simples
        ]

    def clean_namespace(self, tag: str) -> str:
        """
        Remove namespace do nome da tag XML

        Args:
            tag: Nome da tag com namespace

        Returns:
            Nome da tag sem namespace
        """
        return self.namespace_pattern.sub("", tag)

    def clean_all_namespaces(self, data: Dict) -> Dict:
        """
        Remove namespaces de todas as chaves de um dicionário recursivamente

        Args:
            data: Dicionário com dados

        Returns:
            Dicionário com chaves sem namespace
        """
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                cleaned_key = self.clean_namespace(key) if isinstance(key, str) else key
                cleaned[cleaned_key] = self.clean_all_namespaces(value)
            return cleaned
        elif isinstance(data, list):
            return [self.clean_all_namespaces(item) for item in data]
        else:
            return data

    def format_xml_content(self, content: str) -> str:
        """
        Formata conteúdo XML (remove caracteres desnecessários, etc.)

        Args:
            content: Conteúdo XML

        Returns:
            Conteúdo formatado
        """
        # Remove quebras de linha desnecessárias
        content = re.sub(r"\n\s*\n", "\n", content)

        # Remove espaços extras
        content = re.sub(r"[ \t]+", " ", content)

        # Remove espaços no início e fim das linhas
        lines = [line.strip() for line in content.split("\n")]
        content = "\n".join(line for line in lines if line)

        return content.strip()

    def normalize_text(self, text: str) -> str:
        """
        Normaliza texto (remove acentos especiais, caracteres estranhos)

        Args:
            text: Texto para normalizar

        Returns:
            Texto normalizado
        """
        if not text:
            return text

        # Remove caracteres de controle
        text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

        # Normaliza espaços
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def format_monetary_value(self, value: Union[str, float, int]) -> Optional[float]:
        """
        Formata valor monetário brasileiro

        Args:
            value: Valor para formatar

        Returns:
            Valor float formatado ou None se inválido
        """
        if value is None or value == "":
            return None

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            # Remove espaços e caracteres especiais
            value = value.strip().replace(" ", "")

            # Formatos brasileiros com vírgula
            if "," in value and "." in value:
                # Formato: 1.234.567,89
                if value.rfind(",") > value.rfind("."):
                    value = value.replace(".", "").replace(",", ".")
                # Formato: 1,234,567.89
                else:
                    value = value.replace(",", "")
            elif "," in value:
                # Se tem apenas vírgula, assume formato brasileiro
                parts = value.split(",")
                if len(parts) == 2 and len(parts[1]) <= 2:
                    value = value.replace(",", ".")

            try:
                return float(value)
            except ValueError:
                return None

        return None

    def format_cpf_cnpj(self, document: str) -> str:
        """
        Formata CPF ou CNPJ

        Args:
            document: Número do documento

        Returns:
            Documento formatado
        """
        if not document:
            return document

        # Remove caracteres não numéricos
        numbers = re.sub(r"\D", "", document)

        if len(numbers) == 11:  # CPF
            return f"{numbers[:3]}.{numbers[3:6]}.{numbers[6:9]}-{numbers[9:]}"
        elif len(numbers) == 14:  # CNPJ
            return f"{numbers[:2]}.{numbers[2:5]}.{numbers[5:8]}/{numbers[8:12]}-{numbers[12:]}"
        else:
            return document  # Retorna original se não reconhecer

    def format_cep(self, cep: str) -> str:
        """
        Formata CEP brasileiro

        Args:
            cep: CEP para formatar

        Returns:
            CEP formatado
        """
        if not cep:
            return cep

        numbers = re.sub(r"\D", "", cep)

        if len(numbers) == 8:
            return f"{numbers[:5]}-{numbers[5:]}"
        else:
            return cep

    def format_phone(self, phone: str) -> str:
        """
        Formata número de telefone brasileiro

        Args:
            phone: Telefone para formatar

        Returns:
            Telefone formatado
        """
        if not phone:
            return phone

        numbers = re.sub(r"\D", "", phone)

        if len(numbers) == 11:  # Celular com 9
            return f"({numbers[:2]}) {numbers[2:7]}-{numbers[7:]}"
        elif len(numbers) == 10:  # Fixo ou celular sem 9
            return f"({numbers[:2]}) {numbers[2:6]}-{numbers[6:]}"
        else:
            return phone

    def detect_and_format_date(self, date_string: str) -> Optional[str]:
        """
        Detecta e formata data/hora

        Args:
            date_string: String com data

        Returns:
            Data formatada em ISO 8601 ou None se inválida
        """
        if not date_string:
            return None

        # Tenta cada padrão conhecido
        for pattern in self.date_patterns:
            if re.match(pattern, date_string):
                try:
                    # Já está em formato ISO, apenas valida
                    if "T" in date_string:
                        # Remove timezone para parsing se presente
                        clean_date = re.sub(r"[-+]\d{2}:\d{2}$", "", date_string)
                        datetime.fromisoformat(clean_date)
                        return date_string  # Retorna original com timezone
                    else:
                        # Data simples
                        datetime.fromisoformat(date_string)
                        return date_string
                except ValueError:
                    continue

        return None

    def beautify_json(self, data: Dict, indent: int = 2) -> str:
        """
        Formata JSON de forma legível

        Args:
            data: Dados para formatar
            indent: Indentação

        Returns:
            JSON formatado como string
        """
        return json.dumps(
            data,
            indent=indent,
            ensure_ascii=False,
            separators=(",", ": "),
            sort_keys=False,
        )

    def minimize_json(self, data: Dict) -> str:
        """
        Minimiza JSON (sem espaços desnecessários)

        Args:
            data: Dados para minimizar

        Returns:
            JSON minimizado como string
        """
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    def clean_empty_values(
        self,
        data: Any,
        remove_empty_strings: bool = True,
        remove_none: bool = True,
        remove_empty_dicts: bool = True,
        remove_empty_lists: bool = True,
    ) -> Any:
        """
        Remove valores vazios de estrutura de dados

        Args:
            data: Dados para limpar
            remove_empty_strings: Remove strings vazias
            remove_none: Remove valores None
            remove_empty_dicts: Remove dicts vazios
            remove_empty_lists: Remove listas vazias

        Returns:
            Dados limpos
        """
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                cleaned_value = self.clean_empty_values(
                    value,
                    remove_empty_strings,
                    remove_none,
                    remove_empty_dicts,
                    remove_empty_lists,
                )

                # Verifica se deve incluir o valor
                should_include = True

                if remove_none and cleaned_value is None:
                    should_include = False
                elif remove_empty_strings and cleaned_value == "":
                    should_include = False
                elif remove_empty_dicts and cleaned_value == {}:
                    should_include = False
                elif remove_empty_lists and cleaned_value == []:
                    should_include = False

                if should_include:
                    cleaned[key] = cleaned_value

            return cleaned

        elif isinstance(data, list):
            cleaned = []
            for item in data:
                cleaned_item = self.clean_empty_values(
                    item,
                    remove_empty_strings,
                    remove_none,
                    remove_empty_dicts,
                    remove_empty_lists,
                )

                # Inclui item se não for um valor vazio que deve ser removido
                should_include = True

                if remove_none and cleaned_item is None:
                    should_include = False
                elif remove_empty_strings and cleaned_item == "":
                    should_include = False
                elif remove_empty_dicts and cleaned_item == {}:
                    should_include = False
                elif remove_empty_lists and cleaned_item == []:
                    should_include = False

                if should_include:
                    cleaned.append(cleaned_item)

            return cleaned

        else:
            return data

    def get_size_formatted(self, size_bytes: int) -> str:
        """
        Formata tamanho de arquivo em formato legível

        Args:
            size_bytes: Tamanho em bytes

        Returns:
            Tamanho formatado (ex: "1.5 MB")
        """
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math

        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)

        return f"{s} {size_names[i]}"
