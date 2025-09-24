"""
Testes unitários para o XMLToJSONConverter
"""

import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

# Importa módulos do projeto
from src.core.converter import XMLToJSONConverter
from src.utils.validators import XMLValidator
from src.utils.formatters import XMLFormatter


class TestXMLToJSONConverter(unittest.TestCase):
    """Testes para a classe XMLToJSONConverter"""
    
    def setUp(self):
        """Setup executado antes de cada teste"""
        self.converter = XMLToJSONConverter()
        self.sample_xml = '''<?xml version="1.0" encoding="UTF-8"?>
        <root>
            <person id="1">
                <name>João Silva</name>
                <age>30</age>
                <address>
                    <street>Rua das Flores, 123</street>
                    <city>São Paulo</city>
                    <country>Brasil</country>
                </address>
            </person>
        </root>'''
        
        self.nfe_sample_xml = '''<?xml version="1.0" encoding="utf-8"?>
        <nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
            <NFe>
                <infNFe versao="4.00" Id="NFe12345678901234567890123456789012345678901234">
                    <ide>
                        <cUF>35</cUF>
                        <nNF>123456</nNF>
                        <serie>1</serie>
                        <dhEmi>2024-01-15T10:30:00-03:00</dhEmi>
                        <natOp>Venda</natOp>
                    </ide>
                    <emit>
                        <CNPJ>12345678000199</CNPJ>
                        <xNome>Empresa Teste LTDA</xNome>
                    </emit>
                    <dest>
                        <CPF>12345678901</CPF>
                        <xNome>Cliente Teste</xNome>
                    </dest>
                </infNFe>
            </NFe>
        </nfeProc>'''
    
    def test_convert_string_basic(self):
        """Testa conversão básica de string XML"""
        result = self.converter.convert_string(self.sample_xml)
        
        self.assertIsNotNone(result)
        self.assertIn('root', result)
        self.assertIn('person', result['root'])
        
        person = result['root']['person']
        self.assertEqual(person['name'], 'João Silva')
        self.assertEqual(person['age'], 30)  # Deve converter para int
        
    def test_convert_string_with_attributes(self):
        """Testa se preserva atributos XML"""
        result = self.converter.convert_string(self.sample_xml)
        
        person = result['root']['person']
        self.assertIn('@attributes', person)
        self.assertEqual(person['@attributes']['id'], '1')
        
    def test_convert_string_invalid_xml(self):
        """Testa conversão com XML inválido"""
        invalid_xml = "<?xml version='1.0'?><root><unclosed>"
        result = self.converter.convert_string(invalid_xml)
        
        self.assertIsNone(result)
        
    def test_convert_string_empty(self):
        """Testa conversão com string vazia"""
        result = self.converter.convert_string("")
        self.assertIsNone(result)
        
    def test_clean_namespaces_setting(self):
        """Testa configuração de limpeza de namespaces"""
        # Com limpeza de namespaces (padrão)
        result1 = self.converter.convert_string(self.nfe_sample_xml)
        self.assertIn('nfeProc', result1)
        
        # Sem limpeza de namespaces
        config = {'clean_namespaces': False}
        converter_no_clean = XMLToJSONConverter(config=config)
        result2 = converter_no_clean.convert_string(self.nfe_sample_xml)
        
        # Deve manter o namespace no nome da tag
        root_key = list(result2.keys())[0]
        self.assertIn('{http://www.portalfiscal.inf.br/nfe}', root_key)
        
    def test_auto_type_conversion(self):
        """Testa conversão automática de tipos"""
        xml_with_types = '''<?xml version="1.0"?>
        <data>
            <number>123</number>
            <decimal>45.67</decimal>
            <boolean_true>true</boolean_true>
            <boolean_false>false</boolean_false>
            <text>Hello World</text>
        </data>'''
        
        result = self.converter.convert_string(xml_with_types)
        data = result['data']
        
        self.assertEqual(type(data['number']), int)
        self.assertEqual(data['number'], 123)
        
        self.assertEqual(type(data['decimal']), float)
        self.assertEqual(data['decimal'], 45.67)
        
        self.assertEqual(type(data['boolean_true']), bool)
        self.assertTrue(data['boolean_true'])
        
        self.assertEqual(type(data['boolean_false']), bool)
        self.assertFalse(data['boolean_false'])
        
        self.assertEqual(type(data['text']), str)
        self.assertEqual(data['text'], 'Hello World')
        
    def test_convert_file_success(self):
        """Testa conversão de arquivo com sucesso"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as temp_xml:
            temp_xml.write(self.sample_xml)
            temp_xml.flush()
            
            temp_json = temp_xml.name.replace('.xml', '.json')
            
            result = self.converter.convert_file(temp_xml.name, temp_json)
            
            self.assertIsNotNone(result)
            self.assertTrue(Path(temp_json).exists())
            
            # Verifica conteúdo do arquivo JSON
            with open(temp_json, 'r', encoding='utf-8') as f:
                json_content = json.load(f)
                self.assertEqual(json_content, result)
                
            # Cleanup
            Path(temp_xml.name).unlink()
            Path(temp_json).unlink()
            
    def test_convert_file_not_found(self):
        """Testa conversão com arquivo inexistente"""
        result = self.converter.convert_file('arquivo_inexistente.xml')
        self.assertIsNone(result)
        
    def test_convert_batch(self):
        """Testa conversão em lote"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Cria arquivos XML de teste
            xml_files = []
            for i in range(3):
                xml_file = temp_path / f'test_{i}.xml'
                with open(xml_file, 'w', encoding='utf-8') as f:
                    f.write(self.sample_xml)
                xml_files.append(xml_file)
                
            # Converte em lote
            results = self.converter.convert_batch(temp_path)
            
            self.assertEqual(len(results), 3)
            self.assertTrue(all(results.values()))
            
            # Verifica se arquivos JSON foram criados
            for xml_file in xml_files:
                json_file = temp_path / 'converted' / f'{xml_file.stem}.json'
                self.assertTrue(json_file.exists())
                
    def test_custom_configuration(self):
        """Testa configuração personalizada"""
        custom_config = {
            'preserve_attributes': False,
            'auto_type_conversion': False,
            'indent_json': 4
        }
        
        custom_converter = XMLToJSONConverter(config=custom_config)
        result = custom_converter.convert_string(self.sample_xml)
        
        person = result['root']['person']
        
        # Não deve ter atributos
        self.assertNotIn('@attributes', person)
        
        # Não deve converter tipos (age deve ser string)
        self.assertEqual(type(person['age']), str)
        self.assertEqual(person['age'], '30')


class TestXMLValidator(unittest.TestCase):
    """Testes para a classe XMLValidator"""
    
    def setUp(self):
        """Setup executado antes de cada teste"""
        self.validator = XMLValidator()
        self.valid_xml = '''<?xml version="1.0"?><root><item>test</item></root>'''
        self.invalid_xml = '''<?xml version="1.0"?><root><unclosed>'''
        
    def test_valid_xml_string(self):
        """Testa validação de XML válido"""
        result = self.validator.is_valid_xml_string(self.valid_xml)
        self.assertTrue(result)
        
    def test_invalid_xml_string(self):
        """Testa validação de XML inválido"""
        result = self.validator.is_valid_xml_string(self.invalid_xml)
        self.assertFalse(result)
        
    def test_empty_xml_string(self):
        """Testa validação de string vazia"""
        result = self.validator.is_valid_xml_string("")
        self.assertFalse(result)
        
    def test_has_xml_extension(self):
        """Testa verificação de extensão XML"""
        self.assertTrue(self.validator.has_xml_extension('file.xml'))
        self.assertTrue(self.validator.has_xml_extension('file.nfe'))
        self.assertFalse(self.validator.has_xml_extension('file.txt'))
        
    def test_validator_stats(self):
        """Testa estatísticas do validador"""
        # Reset stats
        self.validator.reset_stats()
        
        # Faz algumas validações
        self.validator.is_valid_xml_string(self.valid_xml)
        self.validator.is_valid_xml_string(self.invalid_xml)
        
        stats = self.validator.get_stats()
        
        self.assertEqual(stats['validations_performed'], 2)
        self.assertEqual(stats['valid_files'], 1)
        self.assertEqual(stats['invalid_files'], 1)


class TestXMLFormatter(unittest.TestCase):
    """Testes para a classe XMLFormatter"""
    
    def setUp(self):
        """Setup executado antes de cada teste"""
        self.formatter = XMLFormatter()
        
    def test_clean_namespace(self):
        """Testa limpeza de namespace"""
        tag_with_ns = '{http://example.com/ns}element'
        cleaned = self.formatter.clean_namespace(tag_with_ns)
        self.assertEqual(cleaned, 'element')
        
    def test_format_monetary_value(self):
        """Testa formatação de valores monetários"""
        # Teste com string
        self.assertEqual(self.formatter.format_monetary_value('123.45'), 123.45)
        self.assertEqual(self.formatter.format_monetary_value('1.234,56'), 1234.56)
        
        # Teste com números
        self.assertEqual(self.formatter.format_monetary_value(100), 100.0)
        self.assertEqual(self.formatter.format_monetary_value(100.50), 100.50)
        
        # Teste com valores inválidos
        self.assertIsNone(self.formatter.format_monetary_value(''))
        self.assertIsNone(self.formatter.format_monetary_value(None))
        
    def test_format_cpf_cnpj(self):
        """Testa formatação de CPF/CNPJ"""
        # CPF
        cpf = '12345678901'
        formatted_cpf = self.formatter.format_cpf_cnpj(cpf)
        self.assertEqual(formatted_cpf, '123.456.789-01')
        
        # CNPJ
        cnpj = '12345678000199'
        formatted_cnpj = self.formatter.format_cpf_cnpj(cnpj)
        self.assertEqual(formatted_cnpj, '12.345.678/0001-99')
        
    def test_format_cep(self):
        """Testa formatação de CEP"""
        cep = '12345678'
        formatted_cep = self.formatter.format_cep(cep)
        self.assertEqual(formatted_cep, '12345-678')
        
    def test_clean_empty_values(self):
        """Testa limpeza de valores vazios"""
        data = {
            'valid': 'value',
            'empty_string': '',
            'none_value': None,
            'empty_dict': {},
            'empty_list': [],
            'nested': {
                'keep': 'this',
                'remove': ''
            }
        }
        
        cleaned = self.formatter.clean_empty_values(data)
        
        self.assertIn('valid', cleaned)
        self.assertNotIn('empty_string', cleaned)
        self.assertNotIn('none_value', cleaned)
        self.assertNotIn('empty_dict', cleaned)
        self.assertNotIn('empty_list', cleaned)
        self.assertIn('nested', cleaned)
        self.assertIn('keep', cleaned['nested'])
        self.assertNotIn('remove', cleaned['nested'])


if __name__ == '__main__':
    # Configura nível de log para testes
    import logging
    logging.basicConfig(level=logging.ERROR)
    
    # Executa testes
    unittest.main(verbosity=2)