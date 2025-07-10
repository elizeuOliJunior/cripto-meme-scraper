import schedule
import time
from scraping.coingecko_scraper import coletar_memecoins
from firebase.firebase_client import salvar_dados_meme
from scraping.reddit_scraper import scrape_reddit_data
from firebase.data_retention_manager import delete_old_data 

SUBREDDITS_TO_SCRAPE = ["SatoshiStreetBets", "dogecoin", "ShibainuCoin", "CryptoMoonShots"]

RETENTION_PERIOD_DAYS = 14 

def job_memecoins():
    print("[INFO] Iniciando coleta de dados de memeCoins...")
    dados = coletar_memecoins()

    if not dados:
        print("[INFO] Nenhum dado de memeCoin coletado.")
        return

    for token in dados:
        salvar_dados_meme(token)

    print(f"[INFO] {len(dados)} memeCoins salvos com sucesso.\n")

def job_reddit_sentiment():
    print("[INFO] Iniciando coleta de sentimento do Reddit...")
    scrape_reddit_data(SUBREDDITS_TO_SCRAPE)
    print("[INFO] Coleta de sentimento do Reddit concluída e dados salvos no Firebase.\n")

def job_data_retention():
    print("[INFO] Iniciando processo de retenção de dados...")
    collections_to_clean = ["memecoins", "reddit_posts", "reddit_comments"]
    for collection in collections_to_clean:
        delete_old_data(collection, RETENTION_PERIOD_DAYS)
    print("[INFO] Processo de retenção de dados concluído.\n")

schedule.every(5).minutes.do(job_memecoins)
schedule.every(1).hour.do(job_reddit_sentiment)
schedule.every(1).day.do(job_data_retention)
if __name__ == "__main__":
    print("[SISTEMA] Executando agendador de scraping...\n")

    job_memecoins()         
    job_reddit_sentiment()  
    job_data_retention()    

    while True:
        schedule.run_pending()
        time.sleep(1)