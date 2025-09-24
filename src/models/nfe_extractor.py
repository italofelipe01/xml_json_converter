"""
Extrator específico para Nota Fiscal Eletrônica (NFe) brasileira
"""

from typing import Dict, Optional, List, Any
from datetime import datetime


class NFEExtractor:
    """
    Classe para extrair informações específicas de NFe
    """
    
    def __init__(self):
        """Inicializa o extrator de NFe"""
        self.extracted_count = 0
        
    def extract_nfe_info(self, json_data: Dict) -> Optional[Dict]:
        """
        Extrai informações principais da NFe do JSON convertido
        
        Args:
            json_data: Dados JSON da NFe convertida
            
        Returns:
            Dict com informações extraídas ou None se não for NFe
        """
        try:
            # Navega pela estrutura da NFe
            nfe_proc = json_data.get('nfeProc', {})
            nfe = nfe_proc.get('NFe', {})
            inf_nfe = nfe.get('infNFe', {})
            
            if not inf_nfe:
                return None
                
            # Extrai informações básicas
            info = self._extract_basic_info(inf_nfe)
            
            # Extrai informações do emitente
            emit_info = self._extract_emitente_info(inf_nfe.get('emit', {}))
            if emit_info:
                info.update({'emitente_' + k: v for k, v in emit_info.items()})
                
            # Extrai informações do destinatário
            dest_info = self._extract_destinatario_info(inf_nfe.get('dest', {}))
            if dest_info:
                info.update({'destinatario_' + k: v for k, v in dest_info.items()})
                
            # Extrai totais
            total_info = self._extract_totals_info(inf_nfe.get('total', {}))
            if total_info:
                info.update(total_info)
                
            # Extrai produtos
            produtos_info = self._extract_produtos_info(inf_nfe.get('det', []))
            if produtos_info:
                info.update(produtos_info)
                
            # Extrai informações do protocolo
            prot_info = self._extract_protocolo_info(nfe_proc.get('protNFe', {}))
            if prot_info:
                info.update(prot_info)
                
            self.extracted_count += 1
            return info
            
        except Exception as e:
            print(f"❌ Erro ao extrair informações da NFe: {e}")
            return None
            
    def _extract_basic_info(self, inf_nfe: Dict) -> Dict:
        """Extrai informações básicas da NFe"""
        ide = inf_nfe.get('ide', {})
        
        info = {}
        
        # Informações de identificação
        if 'nNF' in ide:
            info['numero'] = ide['nNF']
        if 'serie' in ide:
            info['serie'] = ide['serie']
        if 'dhEmi' in ide:
            info['data_emissao'] = ide['dhEmi']
        if 'natOp' in ide:
            info['natureza_operacao'] = ide['natOp']
        if 'cUF' in ide:
            info['codigo_uf'] = ide['cUF']
            
        # Chave da NFe dos atributos
        if '@attributes' in inf_nfe and 'Id' in inf_nfe['@attributes']:
            chave = inf_nfe['@attributes']['Id']
            if chave.startswith('NFe'):
                info['chave_nfe'] = chave[3:]  # Remove prefixo NFe
                
        return info
        
    def _extract_emitente_info(self, emit: Dict) -> Dict:
        """Extrai informações do emitente"""
        if not emit:
            return {}
            
        info = {}
        
        if 'xNome' in emit:
            info['nome'] = emit['xNome']
        if 'xFant' in emit:
            info['fantasia'] = emit['xFant']
        if 'CNPJ' in emit:
            info['cnpj'] = self._format_cnpj(emit['CNPJ'])
        if 'CPF' in emit:
            info['cpf'] = self._format_cpf(emit['CPF'])
        if 'IE' in emit:
            info['inscricao_estadual'] = emit['IE']
            
        # Endereço do emitente
        ender_emit = emit.get('enderEmit', {})
        if ender_emit:
            endereco_parts = []
            if 'xLgr' in ender_emit:
                endereco_parts.append(ender_emit['xLgr'])
            if 'nro' in ender_emit:
                endereco_parts.append(ender_emit['nro'])
            if 'xCpl' in ender_emit:
                endereco_parts.append(ender_emit['xCpl'])
                
            if endereco_parts:
                info['endereco'] = ', '.join(endereco_parts)
                
            if 'xBairro' in ender_emit:
                info['bairro'] = ender_emit['xBairro']
            if 'xMun' in ender_emit:
                info['municipio'] = ender_emit['xMun']
            if 'UF' in ender_emit:
                info['uf'] = ender_emit['UF']
            if 'CEP' in ender_emit:
                info['cep'] = self._format_cep(ender_emit['CEP'])
                
        return info
        
    def _extract_destinatario_info(self, dest: Dict) -> Dict:
        """Extrai informações do destinatário"""
        if not dest:
            return {}
            
        info = {}
        
        if 'xNome' in dest:
            info['nome'] = dest['xNome']
        if 'CNPJ' in dest:
            info['cnpj'] = self._format_cnpj(dest['CNPJ'])
        if 'CPF' in dest:
            info['cpf'] = self._format_cpf(dest['CPF'])
            
        # Endereço do destinatário
        ender_dest = dest.get('enderDest', {})
        if ender_dest:
            endereco_parts = []
            if 'xLgr' in ender_dest:
                endereco_parts.append(ender_dest['xLgr'])
            if 'nro' in ender_dest:
                endereco_parts.append(ender_dest['nro'])
            if 'xCpl' in ender_dest:
                endereco_parts.append(ender_dest['xCpl'])
                
            if endereco_parts:
                info['endereco'] = ', '.join(endereco_parts)
                
            if 'xBairro' in ender_dest:
                info['bairro'] = ender_dest['xBairro']
            if 'xMun' in ender_dest:
                info['municipio'] = ender_dest['xMun']
            if 'UF' in ender_dest:
                info['uf'] = ender_dest['UF']
            if 'CEP' in ender_dest:
                info['cep'] = self._format_cep(ender_dest['CEP'])
                
        return info
        
    def _extract_totals_info(self, total: Dict) -> Dict:
        """Extrai informações de totais"""
        if not total:
            return {}
            
        info = {}
        icms_tot = total.get('ICMSTot', {})
        
        if 'vNF' in icms_tot:
            info['valor_total'] = f"R$ {float(icms_tot['vNF']):.2f}"
        if 'vProd' in icms_tot:
            info['valor_produtos'] = f"R$ {float(icms_tot['vProd']):.2f}"
        if 'vICMS' in icms_tot:
            info['valor_icms'] = f"R$ {float(icms_tot['vICMS']):.2f}"
        if 'vIPI' in icms_tot:
            info['valor_ipi'] = f"R$ {float(icms_tot['vIPI']):.2f}"
        if 'vPIS' in icms_tot:
            info['valor_pis'] = f"R$ {float(icms_tot['vPIS']):.2f}"
        if 'vCOFINS' in icms_tot:
            info['valor_cofins'] = f"R$ {float(icms_tot['vCOFINS']):.2f}"
            
        return info
        
    def _extract_produtos_info(self, det: Any) -> Dict:
        """Extrai informações dos produtos"""
        if not det:
            return {}
            
        # det pode ser dict (1 produto) ou list (múltiplos produtos)
        produtos = det if isinstance(det, list) else [det]
        
        info = {
            'quantidade_itens': len(produtos),
            'produtos': []
        }
        
        for produto_det in produtos:
            prod = produto_det.get('prod', {})
            if prod:
                produto_info = {}
                
                if 'xProd' in prod:
                    produto_info['descricao'] = prod['xProd']
                if 'qCom' in prod:
                    produto_info['quantidade'] = float(prod['qCom'])
                if 'uCom' in prod:
                    produto_info['unidade'] = prod['uCom']
                if 'vUnCom' in prod:
                    produto_info['valor_unitario'] = f"R$ {float(prod['vUnCom']):.2f}"
                if 'vProd' in prod:
                    produto_info['valor_total'] = f"R$ {float(prod['vProd']):.2f}"
                if 'NCM' in prod:
                    produto_info['ncm'] = prod['NCM']
                if 'CFOP' in prod:
                    produto_info['cfop'] = prod['CFOP']
                    
                if produto_info:
                    info['produtos'].append(produto_info)
                    
        return info
        
    def _extract_protocolo_info(self, prot_nfe: Dict) -> Dict:
        """Extrai informações do protocolo"""
        if not prot_nfe:
            return {}
            
        info = {}
        inf_prot = prot_nfe.get('infProt', {})
        
        if 'nProt' in inf_prot:
            info['numero_protocolo'] = inf_prot['nProt']
        if 'dhRecbto' in inf_prot:
            info['data_autorizacao'] = inf_prot['dhRecbto']
        if 'cStat' in inf_prot:
            info['status_codigo'] = inf_prot['cStat']
        if 'xMotivo' in inf_prot:
            info['status_descricao'] = inf_prot['xMotivo']
            
        return info
        
    def _format_cnpj(self, cnpj: str) -> str:
        """Formata CNPJ"""
        cnpj_str = str(cnpj)
        if len(cnpj_str) == 14:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        return cnpj
        
    def _format_cpf(self, cpf: str) -> str:
        """Formata CPF"""
        cpf_str = str(cpf)
        if len(cpf_str) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
        
    def _format_cep(self, cep: str) -> str:
        """Formata CEP"""
        cep_str = str(cep)
        if len(cep_str) == 8:
            return f"{cep[:5]}-{cep[5:]}"
        return cep
        
    def extract_summary(self, json_data: Dict) -> Optional[Dict]:
        """
        Extrai resumo executivo da NFe
        
        Args:
            json_data: Dados JSON da NFe
            
        Returns:
            Dict com resumo ou None se erro
        """
        nfe_info = self.extract_nfe_info(json_data)
        
        if not nfe_info:
            return None
            
        # Cria resumo executivo
        summary = {
            'tipo': 'NFe - Nota Fiscal Eletrônica',
            'numero_serie': f"{nfe_info.get('numero', 'N/A')}/{nfe_info.get('serie', 'N/A')}",
            'emitente': nfe_info.get('emitente_nome', 'N/A'),
            'destinatario': nfe_info.get('destinatario_nome', 'N/A'),
            'valor_total': nfe_info.get('valor_total', 'N/A'),
            'data_emissao': nfe_info.get('data_emissao', 'N/A'),
            'status': nfe_info.get('status_descricao', 'N/A'),
            'itens': nfe_info.get('quantidade_itens', 0)
        }
        
        return summary
        
    def get_extraction_stats(self) -> Dict:
        """
        Retorna estatísticas de extração
        
        Returns:
            Dict com estatísticas
        """
        return {
            'nfes_extraidas': self.extracted_count
        }