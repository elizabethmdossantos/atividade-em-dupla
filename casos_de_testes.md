# Documentação dos Testes de Integração e Mocks

Este documento detalha a estratégia de testes automatizados implementada para o módulo de pagamentos (`pagamento.py`). O objetivo principal foi validar a resiliência e o comportamento da função `processar_compra` diante de diferentes respostas do gateway de pagamento, utilizando a técnica de **Mocking** com `pytest-mock` para evitar transações reais e dependência de rede.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Framework:** `pytest`
- **Plugin de Mocking:** `pytest-mock` (utilizando o fixture `mocker`)
- **Biblioteca HTTP:** `requests`

---

## 📐 Estrutura dos Casos de Teste

A suite de testes foi dividida em três cenários críticos de negócio, cobrindo o "Caminho Feliz" (aprovação), uma regra de negócio restritiva (recusa) e uma falha de infraestrutura externa (timeout).

### 📋 Tabela Resumo dos Desafios

| Caso de Teste / Desafio | Alvo do Mock | Comportamento Simulado | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **1. Compra Aprovada** | `src.pagamento.enviar_para_gateway` | Dicionário com `status: "aprovado"` e ID da transação | Mensagem de sucesso com o código da transação. |
| **2. Cliente Sem Limite** | `src.pagamento.enviar_para_gateway` | Dicionário com `status: "recusado"` e motivo | Mensagem informando a recusa e o motivo específico. |
| **3. Black Friday (Timeout)** | `src.pagamento.requests.post` | Lançamento da exceção `requests.exceptions.Timeout` | Mensagem de orientação para o usuário verificar a fatura. |

---

## 🔍 Detalhamento dos Cenários

### Desafio 1: A Compra Aprovada (O Caminho Feliz)
* **Objetivo:** Garantir que o fluxo principal funciona corretamente quando o gateway processa o pagamento com sucesso.
* **Estratégia de Mock:** Interceptou-se a função interna `enviar_para_gateway` para retornar um dicionário simulando a aprovação da operadora do cartão. Isso impede que uma requisição HTTP real seja disparada e evita cobranças indevidas.
* **Validação:** O teste garante que o identificador da transação (`transacao_id`) é extraído corretamente e exibido na mensagem final de sucesso.

### Desafio 2: Cliente Sem Limite (Mock de Retorno Específico)
* **Objetivo:** Validar o tratamento de respostas negativas controladas vindas do gateway (regras de negócio do cartão).
* **Estratégia de Mock:** Interceptou-se a função `enviar_para_gateway` alterando o payload de retorno para `status: "recusado"` e definindo o motivo como `"Saldo insuficiente"`.
* **Validação:** O teste certifica que o sistema não quebra ao receber uma recusa e consegue tratar e repassar o motivo amigável para o usuário final.

### Desafio 3: A Black Friday (Mock de Exceção Direto no requests)
* **Objetivo:** Testar a tolerância a falhas de infraestrutura da aplicação quando o parceiro externo sofre com sobrecarga e fica indisponível (gerando estouro de tempo).
* **Estratégia de Mock:** Diferente dos anteriores, este teste faz o mock diretamente na biblioteca de mais baixo nível: `requests.post`. Utilizou-se a propriedade `side_effect` do mock para injetar/lançar a exceção física `requests.exceptions.Timeout()`.
* **Validação:** O teste comprova que o bloco `try/except` da aplicação captura corretamente o erro de rede e devolve uma mensagem de segurança instruindo o cliente a checar a fatura antes de tentar novamente, prevenindo a duplicidade de compras.

---

## 🚀 Como Executar os Testes

Para rodar a suite de testes localmente e verificar a cobertura dos cenários documentados, certifique-se de ter as dependências instaladas e execute o comando abaixo na raiz do projeto:

```bash
# Instalação das dependências necessárias
pip install pytest pytest-mock requests

# Execução dos testes
pytest -v