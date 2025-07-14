import firebase_admin
from firebase_admin import credentials, db
import os
import json
import base64
from dotenv import load_dotenv

load_dotenv()

# Inicializa o Firebase apenas uma vez
if not firebase_admin._apps:
    service_account_key_base64 = os.getenv('SERVICE_ACCOUNT_KEY_BASE64')

    if not service_account_key_base64:
        raise EnvironmentError("[ERRO] Variável de ambiente SERVICE_ACCOUNT_KEY_BASE64 não está definida.")

    try:
        service_account_info = json.loads(
            base64.b64decode(service_account_key_base64).decode("utf-8")
        )
        cred = credentials.Certificate(service_account_info)
    except Exception as e:
        raise ValueError(f"[ERRO] Falha ao decodificar SERVICE_ACCOUNT_KEY_BASE64: {e}")

    firebase_admin.initialize_app(cred, {
        "databaseURL": os.getenv("FIREBASE_DB_URL")
    })
    print("[FIREBASE] Inicializado com credenciais da variável de ambiente.")

def salvar_dados_meme(token_data):
    ref = db.reference("/memecoins")
    ref.push(token_data)
    print(f"[FIREBASE] Token '{token_data['nome']}' salvo com sucesso.")

def salvar_dados_reddit(data, data_type):
    ref = db.reference(f"/reddit_{data_type}")
    ref.push(data)
    print(f"[FIREBASE] {data_type.capitalize()} do Reddit salvo com sucesso.")