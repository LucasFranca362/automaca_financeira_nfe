import gspread
from google.oauth2.service_account import Credentials

class PlanilhaFinanceira:
    def __init__(self, caminho_credenciais, id_planilha):
        # Escopos de autorização da API
        escopos = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credenciais = Credentials.from_service_account_file(caminho_credenciais, scopes=escopos)
        self.cliente = gspread.authorize(credenciais)
        self.planilha = self.cliente.open_by_key(id_planilha)
        
        # Conecta exatamente na aba 'Mercadorias'
        self.aba_mercadorias = self.planilha.worksheet('Mercadorias')

    def verificar_nota_existente(self, num_nota):
        # Puxa a coluna A (índice 1)
        lista_notas = self.aba_mercadorias.col_values(1)
        if str(num_nota) in lista_notas:
            return True
        else:
            return False

    def adicionar_boleto(self, num_nota, fornecedor, parcela, vencimento, valor, data_emissao):
        # Organiza a lista na ordem exata das colunas da aba Mercadorias
        nova_linha = [num_nota, fornecedor, parcela, vencimento, valor, "Pendente", data_emissao]
        self.aba_mercadorias.append_row(nova_linha)