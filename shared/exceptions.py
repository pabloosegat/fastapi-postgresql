class FornecedorNotFound(Exception):
    """Exceção lançada quando um fornecedor não é encontrado no banco de dados."""
    
    def __init__(self, message="Fornecedor não encontrado no banco de dados."):
        self.message = message
        super().__init__(self.message)

class ContaNotFound(Exception):
    """Exceção lançada quando uma conta pagar e receber não é encontrada no banco de dados."""
    
    def __init__(self, message="Conta não encontrada no banco de dados."):
        self.message = message
        super().__init__(self.message)

class MonthlyAccountLimitExceededException(Exception):
    """Exceção lançada quando o limite de contas criadas em um mês é excedido."""
    
    def __init__(self, message="Limite máximo de contas criadas neste mês foi atingido."):
        self.message = message
        super().__init__(self.message)