import firebase_admin
from firebase_admin import credentials, db
import os
import json
import base64

from config import FIREBASE_DB_URL

# Inicializa o Firebase apenas uma vez
if not firebase_admin._apps:
    # Tenta carregar a chave da variável de ambiente base64
    service_account_key_base64 = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_BASE64")
    if service_account_key_base64:
        try:
            # Decodifica a string base64 para JSON
            service_account_info = json.loads(base64.b64decode(service_account_key_base64).decode("utf-8"))
            cred = credentials.Certificate(service_account_info)
        except Exception as e:
            print(f"Erro ao decodificar FIREBASE_SERVICE_ACCOUNT_KEY_BASE64: {e}")
            # Fallback para arquivo local se a variável de ambiente falhar (para desenvolvimento local)
            cred = credentials.Certificate("serviceAccountKey.json")
    else:
        # Fallback para arquivo local se a variável de ambiente não estiver definida
        cred = credentials.Certificate("serviceAccountKey.json")

    firebase_admin.initialize_app(cred, {
        "databaseURL": FIREBASE_DB_URL
    })

# Função para salvar um token no Realtime Database
def salvar_dados_meme(token_data):
    ref = db.reference("/memecoins")
    ref.push(token_data)
    print(f"[FIREBASE] Token \'{token_data['nome']}\' salvo com sucesso.")

def salvar_dados_reddit(data, data_type):
    # data_type pode ser 'posts' ou 'comments'
    ref = db.reference(f"/reddit_{data_type}")
    ref.push(data)
    print(f"[FIREBASE] {data_type.capitalize()} do Reddit salvo com sucesso.")
