import xlwings as xw
import time
from datetime import datetime
import config
from database import fetch_live_adjustments

def setup_dashboard(ws):
    """Prepara a interface visual do Excel via xlwings."""
    ws.clear()
    ws.range('A1:E1').merge()
    ws.range('A1').value = '📦 LIVE INVENTORY MONITOR'
    ws.range('A1').api.Font.Bold = True
    ws.range('A1').api.Font.Size = 16
    
    ws.range('A3').value = ['TIMESTAMP', 'SKU', 'ADJUSTED_QTY', 'STATUS']
    ws.range('A3:D3').api.Font.Bold = True
    ws.range('A3:D3').color = (200, 200, 200)

def update_live_dashboard():
    """Roda como um Daemon conectando ao Excel ativo e atualizando via DB."""
    print("Iniciando Live Monitor... Abra um Excel em branco e chame a aba de 'Dashboard'.")
    
    try:
        # Tenta se conectar à planilha ativa chamada 'Dashboard'
        wb = xw.books.active
        if 'Dashboard' not in [s.name for s in wb.sheets]:
            wb.sheets.add('Dashboard')
        ws = wb.sheets['Dashboard']
    except Exception as e:
        print(f"Erro ao conectar ao Excel. Certifique-se que o Excel está aberto. {e}")
        return

    setup_dashboard(ws)

    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ws.range('E1').value = f"Last Update: {now}"
            
            # Busca dados reais do banco
            df_live = fetch_live_adjustments()
            
            if not df_live.empty:
                # Limpa a tabela anterior e escreve os dados novos rapidamente
                ws.range('A4:D1000').clear_contents()
                ws.range('A4').value = df_live[['created_at', 'sku', 'adjusted_qty', 'status']].values
            else:
                ws.range('A4').value = "Waiting for adjustments..."
                
            time.sleep(10) # Polling interval
            
        except KeyboardInterrupt:
            print("\nMonitor encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"Erro no ciclo de atualização: {e}")
            time.sleep(10)

if __name__ == "__main__":
    update_live_dashboard()