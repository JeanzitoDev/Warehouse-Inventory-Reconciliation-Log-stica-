import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "data" / "output"
ERP_UPLOADS_DIR = OUTPUT_DIR / "erp_uploads"

# Cria diretórios se não existirem
for directory in [INPUT_DIR, OUTPUT_DIR, ERP_UPLOADS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

DB_URL = os.getenv("DATABASE_URL", "sqlite:///warehouse.db")

# Regras de Negócio (Exemplo: Categorias de discrepância de estoque)
DISCREPANCY_RULES = {
    'DAMAGE': {'max_tolerance': 5.0, 'color': 'FF0000'},   # Vermelho
    'MISSING': {'max_tolerance': 2.0, 'color': 'FFA500'},  # Laranja
    'SURPLUS': {'max_tolerance': 10.0, 'color': '008000'}  # Verde
}