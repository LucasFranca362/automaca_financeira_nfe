import xml.etree.ElementTree as ET
import os

def extrair_dados_nfe(caminho_arquivo_xml):
    """
    Lê o XML de uma NF-e e extrai os dados necessários para a planilha.
    Retorna uma lista de dicionários, onde cada dicionário é uma parcela (boleto).
    """
    # Todo XML da Sefaz exige o mapeamento deste namespace para que o Python encontre as tags
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    
    try:
        tree = ET.parse(caminho_arquivo_xml)
        root = tree.getroot()
        
        # 1. Dados Gerais da Nota
        num_nota = root.find('.//nfe:ide/nfe:nNF', ns).text
        
        # A Sefaz envia a data no formato AAAA-MM-DDTHH:MM:SS-03:00. Vamos isolar o dia:
        data_emissao_crua = root.find('.//nfe:ide/nfe:dhEmi', ns).text[:10]
        # Transforma AAAA-MM-DD em DD/MM/AAAA para a planilha
        data_emissao = "/".join(data_emissao_crua.split("-")[::-1])
        
        # 2. Dados do Fornecedor (Emitente)
        fornecedor = root.find('.//nfe:emit/nfe:xNome', ns).text
        
        # 3. Dados de Cobrança e Parcelas (Duplicatas)
        duplicatas = root.findall('.//nfe:cobr/nfe:dup', ns)
        total_parcelas = len(duplicatas)
        
        dados_faturamento = []
        
        # Se a nota não tiver parcelas (foi paga à vista, por exemplo)
        if total_parcelas == 0:
            # Você pode tratar aqui se deseja lançar como parcela única ou ignorar
            pass
            
        for i, dup in enumerate(duplicatas):
            # Isola e formata o vencimento da parcela (AAAA-MM-DD para DD/MM/AAAA)
            venc_cruo = dup.find('nfe:dVenc', ns).text
            vencimento = "/".join(venc_cruo.split("-")[::-1])
            
            valor_parcela = dup.find('nfe:vDup', ns).text
            
            # Monta a estrutura exatamente igual às colunas da aba Mercadorias
            dados_faturamento.append({
                "Nº da Nota": num_nota,
                "Fornecedor": fornecedor,
                "Parcela": f"{i + 1}/{total_parcelas}",
                "Vencimento": vencimento,
                "Valor": float(valor_parcela),
                "Data de Emissão": data_emissao
            })
            
        return dados_faturamento

    except Exception as e:
        print(f"Erro ao processar o arquivo XML: {e}")
        return []

# --- Área de Testes Local ---
if __name__ == "__main__":
    # Se você tiver algum XML real de alguma compra antiga no seu PC, 
    # jogue na pasta do projeto e mude o nome abaixo para testar o print
    caminho_teste = "nota_exemplo.xml"
    
    if os.path.exists(caminho_teste):
        resultado = extrair_dados_nfe(caminho_teste)
        for parcela in resultado:
            print(parcela)
    else:
        print(f"Para testar, coloque um arquivo XML válido nomeado como '{caminho_teste}' nesta pasta.")