import json
import os 
from xml_parser import extrair_dados_nfe
from planilha_manager import PlanilhaFinanceira

def rodar_automacao():
    print("Iniciando robô financeiro...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_json = os.path.join(base_dir, 'credentials.json')
    caminho_config = os.path.join(base_dir, 'config.json')
    with open(caminho_config, 'r') as arquivo:
        config = json.load(arquivo)
    
    id_planilha = config['ID_PLANILHA']
    caminho_xml = os.path.join(base_dir, 'nota_exemplo.xml')

    print("Conectando com Google Sheets")
    gerenciador = PlanilhaFinanceira(caminho_json, id_planilha)

    print(f"Lendo o arquivo XML: {caminho_xml}...")
    parcelas = extrair_dados_nfe(caminho_xml)
    if not parcelas:
        print("Nenhum dado encontrado ou erro na leitura")
        return 
    num_nota_atual = parcelas[0]['Nº da Nota']
    print(f"Verificando se a Nota {num_nota_atual} já existe...")

    if gerenciador.verificar_nota_existente(num_nota_atual):
        print(f"Aviso: A nota fiscal {num_nota_atual} já foi lançada anteriormente")
    else:
        print("Nova nota identificada! Inserindo parcelas no sistema...")
        for boleto in parcelas:
            gerenciador.adicionar_boleto(
                num_nota=boleto['Nº da Nota'],
                fornecedor=boleto['Fornecedor'],
                parcela=boleto['Parcela'],
                vencimento=boleto['Vencimento'],
                valor=boleto['Valor'],
                data_emissao=boleto['Data de Emissão']
            )
        print("Integração concluída com sucesso!")

if __name__ == "__main__":
    rodar_automacao()
