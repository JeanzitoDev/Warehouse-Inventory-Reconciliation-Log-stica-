import pandas as pd
from pathlib import Path
import config
from datetime import datetime

def generate_erp_payload(reconciled_filename: str):
    """
    Gera arquivo de integração em lote (Bulk Upload) para o ERP genérico.
    Converte o layout amigável para o layout estrito exigido pela API/Sistema de estoque.
    """
    input_path = config.OUTPUT_DIR / reconciled_filename
    
    if not input_path.exists():
        print(f"Arquivo não encontrado: {input_path}")
        return

    df = pd.read_excel(input_path, sheet_name="Reconciliation")
    
    # Filtra apenas o que precisa de ajuste
    df_adjustments = df[df['status'] != 'OK'].copy()
    
    if df_adjustments.empty:
        print("Nenhuma divergência encontrada. Upload não é necessário.")
        return

    # Mapeamento e transformação estrita (ETL final)
    upload_rows = []
    
    for _, row in df_adjustments.iterrows():
        # Regra de negócio: Diferença de sistemas
        reason_code = 'INV_MISSING' if row['discrepancy'] < 0 else 'INV_SURPLUS'
        
        upload_rows.append({
            'WAREHOUSE_ID': 'WH-001',
            'ITEM_SKU': str(row['sku']).upper().strip(),
            'ADJUSTMENT_TYPE': 'DELTA',
            'QUANTITY': abs(row['discrepancy']), # Sistema exige valor absoluto
            'SIGN': '-' if row['discrepancy'] < 0 else '+',
            'REASON_CODE': reason_code,
            'TRANSACTION_DATE': datetime.now().strftime("%Y%m%d")
        })

    df_payload = pd.DataFrame(upload_rows)
    
    # Salva no formato estrito (CSV sem formatação visual)
    output_filename = f"ERP_SYNC_WH001_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output_path = config.ERP_UPLOADS_DIR / output_filename
    
    df_payload.to_csv(output_path, index=False, sep=';')
    print(f"✅ Arquivo de Bulk Upload gerado para o ERP: {output_path.name}")
    print(f"Total de registros para processamento: {len(df_payload)}")

if __name__ == "__main__":
    generate_erp_payload("Reconciled_physical_count_week12.xlsx")