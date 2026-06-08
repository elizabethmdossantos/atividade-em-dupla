import pytest
import requests
from src.pagamento import processar_compra

def test_processar_compra_aprovada(mocker):
    """
    Desafio 1: Testa o fluxo onde o cartão tem limite e a compra é aprovada.
    """
    mock_gateway = mocker.patch("src.pagamento.enviar_para_gateway")
    
    mock_gateway.return_value = {
        "status": "aprovado",
        "transacao_id": "INGRESSO-998877"
    }
    
    resultado = processar_compra(usuario_id=1, dados_cartao={"numero": "1234"}, valor=150.0)
    
    assert resultado == "Sucesso! Transação INGRESSO-998877 confirmada."

def test_processar_compra_recusada_sem_limite(mocker):
    """
    Desafio 2: Testa o fluxo onde o cartão é recusado por falta de limite.
    """
    mock_gateway = mocker.patch("src.pagamento.enviar_para_gateway")
    
    mock_gateway.return_value = {
        "status": "recusado",
        "motivo": "Saldo insuficiente"
    }
    
    resultado = processar_compra(usuario_id=1, dados_cartao={"numero": "1234"}, valor=5000.0)
    
    assert resultado == "Pagamento recusado. Motivo: Saldo insuficiente."

def test_processar_compra_timeout_na_black_friday(mocker):
    """
    Desafio 3: Testa o comportamento do sistema quando a API cai por Timeout.
    """
    mock_post = mocker.patch("src.pagamento.requests.post")
    
    mock_post.side_effect = requests.exceptions.Timeout()
    
    resultado = processar_compra(usuario_id=1, dados_cartao={"numero": "1234"}, valor=100.0)
    
    mensagem_esperada = "Tempo de resposta esgotado. Verifique sua fatura antes de tentar de novo."
    assert resultado == mensagem_esperada