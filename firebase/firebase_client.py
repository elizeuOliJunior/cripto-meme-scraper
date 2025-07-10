import firebase_admin
from firebase_admin import credentials, db
import os
from config import FIREBASE_DB_URL

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": FIREBASE_DB_URL
    })

def salvar_dados_meme(token_data):
    ref = db.reference("/memecoins")
    ref.push(token_data)
    print(f"[FIREBASE] Token '{token_data['nome']}' salvo com sucesso.")


def salvar_dados_reddit(data, data_type):
    ref = db.reference(f"/reddit_{data_type}")
    ref.push(data)
    print(f"[FIREBASE] {data_type.capitalize()} do Reddit salvo com sucesso.")
