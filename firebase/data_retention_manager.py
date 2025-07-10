import firebase_admin
from firebase_admin import credentials, db
import datetime
import os
from config import FIREBASE_DB_URL

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": FIREBASE_DB_URL
    })

def delete_old_data(ref_path, retention_days):
    print(f"[RETENÇÃO] Verificando dados antigos em /{ref_path}...")
    ref = db.reference(ref_path)
    
    limit_date = datetime.datetime.now() - datetime.timedelta(days=retention_days)
    limit_timestamp_str = limit_date.strftime("%Y-%m-%dT%H:%M:%S") # Formato ISO para comparação

    all_data = ref.get()

    if not all_data:
        print(f"[RETENÇÃO] Nenhuma dado encontrado em /{ref_path}.")
        return

    deleted_count = 0
    for key, value in all_data.items():
        timestamp_str = value.get("timestamp")
        if not timestamp_str:
            continue
        
        try:
            if "." in timestamp_str:
                item_datetime = datetime.datetime.strptime(timestamp_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")
            else:
                item_datetime = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")

            if item_datetime < limit_date:
                ref.child(key).delete()
                deleted_count += 1
                print(f"[RETENÇÃO] Deletado: {ref_path}/{key} (Timestamp: {timestamp_str})")
        except ValueError:
            print(f"[RETENÇÃO] Aviso: Timestamp inválido para {ref_path}/{key}: {timestamp_str}")
            continue

    print(f"[RETENÇÃO] Concluída a limpeza em /{ref_path}. Total de itens deletados: {deleted_count}")

if __name__ == "__main__":
    RETENTION_PERIOD_DAYS = 14 
    
    collections_to_clean = ["memecoins", "reddit_posts", "reddit_comments"]

    for collection in collections_to_clean:
        delete_old_data(collection, RETENTION_PERIOD_DAYS)
    print("[RETENÇÃO] Processo de retenção de dados concluído para todas as coleções.")
