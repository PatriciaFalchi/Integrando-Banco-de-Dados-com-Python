# Integrando Banco de Dados com Python

# Sistema de Cadastro Bancário com SQLAlchemy

Este projeto simula um sistema bancário simples com uso de **Python** e **SQLAlchemy ORM**, no qual é possível cadastrar clientes e suas respectivas contas bancárias (corrente ou poupança), armazenar esses dados em um banco SQLite em memória e realizar consultas estruturadas.

## 📚 Tecnologias Utilizadas

- Python 3.x  
- SQLAlchemy (ORM)
- SQLite (banco de dados em memória)

## Estrutura do Projeto

O projeto contém duas classes principais mapeadas como tabelas:

### 🔹 `Cliente`

Campos:
- `id`: identificador único
- `nome`: nome do cliente
- `cpf`: CPF do cliente
- `endereco`: endereço do cliente  
Relacionamento:
- `conta`: relacionamento um-para-muitos com a tabela Conta

### 🔹 `Conta`

Campos:
- `id_conta`: identificador da conta
- `tipo`: tipo da conta (corrente ou poupança)
- `agencia`: número da agência
- `numero`: número da conta
- `saldo`: saldo disponível  
Chave estrangeira:
- `id_cliente`: referencia o cliente titular da conta

## ⚙️ Funcionalidades

- Criação das tabelas `cliente_account` e `conta` no SQLite em memória
- Inserção de dados de exemplo (5 clientes e suas contas)
- Execução de consultas:
  - Filtro por nome
  - Ordenação alfabética
  - Junção de tabelas para exibir nome do cliente e saldo
  - Contagem de clientes cadastrados

## 🔍 Exemplos de Consulta

```python
# Clientes cujo nome é 'mateus'
stmt = select(Cliente).where(Cliente.nome.in_(['mateus']))

# Ordenar clientes pelo nome
stmt_order = select(Cliente).order_by(Cliente.nome)

# Junção entre Cliente e Conta
stmt_join = select(Cliente.nome, Conta.saldo).join_from(Cliente, Conta)

# Contagem de registros na tabela Cliente
stmt_count = select(func.count('*')).select_from(Cliente)
