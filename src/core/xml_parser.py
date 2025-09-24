"""
Módulo de parsing XML
"""

import xml.etree.ElementTree as ET
from typing import Dict, Optional, Any, Union
from collections import OrderedDict

from ..utils.formatters import XMLFormatter


class XMLParser:
    """
    Classe para parsing de XML
    """
    
    def __init__(self):
        """Inicializa o parser"""
        self.formatter = XMLFormatter()
        self.stats = {
            'parsed_elements': 0,
            'parse_errors': 0
        }
        
    def parse_string(self, xml_string: str) -> Optional[ET.Element]:
        """
        Faz parse de string XML
        
        Args:
            xml_string: String contendo XML
            
        Returns:
            Elemento raiz ou None em caso de erro
        """
        try:
            root = ET.fromstring(xml_string)
            self.stats['parsed_elements'] += 1
            return root
        except ET.ParseError as e:
            print(f"❌ Erro no parse XML: {e}")
            self.stats['parse_errors'] += 1
            return None
        except Exception as e:
            print(f"❌ Erro inesperado no parse: {e}")
            self.stats['parse_errors'] += 1
            return None
            
    def parse_file(self, xml_path: str) -> Optional[ET.Element]:
        """
        Faz parse de arquivo XML
        
        Args:
            xml_path: Caminho do arquivo XML
            
        Returns:
            Elemento raiz ou None em caso de erro
        """
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            self.stats['parsed_elements'] += 1
            return root
        except ET.ParseError as e:
            print(f"❌ Erro no parse do arquivo XML: {e}")
            self.stats['parse_errors'] += 1
            return None
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {xml_path}")
            self.stats['parse_errors'] += 1
            return None
        except Exception as e:
            print(f"❌ Erro inesperado no parse do arquivo: {e}")
            self.stats['parse_errors'] += 1
            return None
            
    def element_to_dict(self, element: ET.Element, settings: Dict) -> Union[Dict, str, None]:
        """
        Converte elemento XML para dicionário
        
        Args:
            element: Elemento XML
            settings: Configurações de conversão
            
        Returns:
            Dicionário, string ou None
        """
        result = OrderedDict() if settings.get('preserve_order', True) else {}
        
        # Adiciona atributos
        if element.attrib and settings.get('preserve_attributes', True):
            result['@attributes'] = dict(element.attrib)
            
        # Processa elementos filhos
        children = list(element)
        if children:
            children_dict = OrderedDict() if settings.get('preserve_order', True) else {}
            
            for child in children:
                # Limpa namespace se configurado
                child_tag = (self.formatter.clean_namespace(child.tag) 
                           if settings.get('clean_namespaces', True) 
                           else child.tag)
                
                child_data = self.element_to_dict(child, settings)
                
                # Trata elementos com mesmo nome (cria lista)
                if child_tag in children_dict:
                    if not isinstance(children_dict[child_tag], list):
                        children_dict[child_tag] = [children_dict[child_tag]]
                    children_dict[child_tag].append(child_data)
                else:
                    children_dict[child_tag] = child_data
                    
            # Se tem texto e filhos, adiciona o texto como '_text'
            if element.text and element.text.strip():
                result['_text'] = element.text.strip()
                
            result.update(children_dict)
            
        else:
            # Elemento sem filhos - apenas texto
            text = element.text.strip() if element.text else ''
            
            if text:
                if result:  # Se já tem atributos
                    result['_value'] = self._convert_value_type(text, settings)
                else:  # Se não tem atributos, retorna apenas o valor
                    return self._convert_value_type(text, settings)
            elif not result:  # Sem texto nem atributos
                return None
                
        return result if result else None
        
    def _convert_value_type(self, value: str, settings: Dict) -> Union[str, int, float, bool, None]:
        """
        Converte string para tipo apropriado
        
        Args:
            value: Valor string
            settings: Configurações de conversão
            
        Returns:
            Valor convertido para tipo apropriado
        """
        if not settings.get('auto_type_conversion', True):
            return value
            
        # Valor vazio
        if not value:
            return None
            
        # Boolean
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
            
        # Número inteiro
        if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
            try:
                return int(value)
            except ValueError:
                pass
                
        # Número decimal
        try:
            if '.' in value or ',' in value:
                # Tenta formato brasileiro (vírgula como decimal)
                if ',' in value and value.count(',') == 1:
                    value_normalized = value.replace(',', '.')
                else:
                    value_normalized = value
                    
                return float(value_normalized)
        except ValueError:
            pass
            
        # Retorna string original se não conseguiu converter
        return value
        
    def extract_namespaces(self, element: ET.Element) -> Dict[str, str]:
        """
        Extrai namespaces do elemento XML
        
        Args:
            element: Elemento XML
            
        Returns:
            Dict com mapeamento de prefixos e URIs de namespace
        """
        namespaces = {}
        
        # Verifica o elemento atual
        if '}' in element.tag:
            uri = element.tag.split('}')[0][1:]  # Remove { do início
            prefix = element.prefix or 'default'
            namespaces[prefix] = uri
            
        # Verifica elementos filhos recursivamente
        for child in element:
            child_namespaces = self.extract_namespaces(child)
            namespaces.update(child_namespaces)
            
        return namespaces
        
    def get_element_path(self, element: ET.Element, clean_ns: bool = True) -> str:
        """
        Gera caminho XPath-like do elemento
        
        Args:
            element: Elemento XML
            clean_ns: Se deve limpar namespaces
            
        Returns:
            String com o caminho do elemento
        """
        path_parts = []
        current = element
        
        while current is not None:
            tag = (self.formatter.clean_namespace(current.tag) 
                  if clean_ns else current.tag)
            path_parts.append(tag)
            current = current.getparent() if hasattr(current, 'getparent') else None
            
        return '/' + '/'.join(reversed(path_parts))
        
    def get_stats(self) -> Dict:
        """
        Retorna estatísticas do parser
        
        Returns:
            Dict com estatísticas
        """
        return self.stats.copy()
        
    def reset_stats(self):
        """Reset das estatísticas"""
        self.stats = {
            'parsed_elements': 0,
            'parse_errors': 0
        }