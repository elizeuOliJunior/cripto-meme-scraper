import schedule
import time
from scraping.coingecko_scraper import coletar_memecoins
from firebase.firebase_client import salvar_dados_meme

def job():
    print("[INFO] Iniciando coleta de dados...")
    dados = coletar_memecoins()

    if not dados:
        print("[INFO] Nenhum dado coletado.")
        return

    for token in dados:
        salvar_dados_meme(token)

    print(f"[INFO] {len(dados)} tokens salvos com sucesso.\n")

# Agendar para rodar a cada 5 minutos
schedule.every(5).minutes.do(job)

if __name__ == "__main__":
    print("[SISTEMA] Executando agendador de scraping...\n")
    job()  # Roda a primeira vez imediatamente
    while True:
        schedule.run_pending()
        time.sleep(1)
