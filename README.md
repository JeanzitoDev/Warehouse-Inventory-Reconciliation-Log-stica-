# Warehouse Inventory Sync & Live Monitor

Sistema completo de engenharia de dados e automação logística desenvolvido em Python. Este projeto gerencia o fluxo de reconciliação de estoque (Inventário Físico vs. ERP), cria um monitor de operações ao vivo dentro do Excel e gera arquivos de integração em lote (*Bulk Uploads*) para sincronização com o ERP principal.

## 🚀 Arquitetura da Solução

O projeto é dividido em três *Jobs* principais:

1. **Inventory Reconciliation (`01_reconcile_stock.py`):** Motor de regras que cruza as planilhas de contagem física preenchidas pelos operadores do armazém com o banco de dados (PostgreSQL) do sistema central. Gera relatórios com formatação condicional (*Headless Excel manipulation* via `openpyxl`).
2. **Live Dashboard Daemon (`02_live_dashboard.py`):** Um script de *polling* que consome dados transacionais do banco de dados e atualiza dinamicamente a interface gráfica de uma planilha Excel aberta em tempo real, utilizando a biblioteca `xlwings`.
3. **ERP Bulk Payload Generator (`03_generate_erp_upload.py`):** Módulo de extração final (ETL) que mapeia as divergências aprovadas para um leiaute estrito (CSV Posicional) exigido para ingestão massiva no ERP corporativo.

## 🛠️ Tecnologias Utilizadas

- **Core:** `Python 3.10+`, `pandas` para processamento tabular vetorizado.
- **Integração de Banco de Dados:** `SQLAlchemy` e driver nativo para conexão relacional. Implementação de resiliência (*Retry Pattern/Exponential Backoff*) utilizando `tenacity`.
- **Automação de Planilhas:** 
  - `openpyxl`: Geração e formatação de arquivos em *background* (sem depender do pacote Office instalado).
  - `xlwings`: Comunicação COM interativa (Windows/Mac) para construir UIs dinâmicas no Excel.

## ⚙️ Instalação e Execução

Pré-requisitos: Python 3.10+ e Microsoft Excel (para o módulo Live Dashboard).

**1. Clone o repositório:**

```bash
git clone [https://github.com/seu-usuario/warehouse-inventory-sync.git](https://github.com/seu-usuario/warehouse-inventory-sync.git)

cd warehouse-inventory-sync
```

**2. Crie e ative o ambiente virtual:**

No Linux/macOS:

```python
python -m venv venv
source venv/bin/activate
```

No Windows:

```python
python -m venv venv
venv\Scripts\activate
```

**3. Instale as dependências:**

```python
pip install -r requirements.txt
```

**4. Execute os módulos (Exemplos):**

```python
# Executa a reconciliação (Geração do relatório)
python src/01_reconcile_stock.py

# Inicia o monitor ao vivo (Abra um Excel em branco antes de executar)
python src/02_live_dashboard.py
```