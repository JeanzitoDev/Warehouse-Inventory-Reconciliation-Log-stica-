import pandas as pd
from sqlalchemy import create_engine, text
from tenacity import retry, stop_after_attempt, wait_exponential
import config

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_engine():
    """Garante conexão resiliente com o banco de dados do ERP logístico."""
    return create_engine(config.DB_URL)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=5))
def fetch_system_inventory(category: str = None) -> pd.DataFrame:
    """Busca o saldo teórico de estoque no sistema."""
    engine = get_engine()
    
    query = """
        SELECT sku, product_name, system_qty, location_zone
        FROM inventory_balances
        WHERE status = 'ACTIVE'
    """
    
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
        return df

def fetch_live_adjustments() -> pd.DataFrame:
    """Simula a busca de chamados/ajustes em tempo real para o painel de controle."""
    engine = get_engine()
    query = """
        SELECT adjustment_id, sku, adjusted_qty, status, created_at
        FROM stock_adjustments
        WHERE DATE(created_at) = CURRENT_DATE
        ORDER BY created_at DESC
    """
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)