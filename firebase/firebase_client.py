import firebase_admin
from firebase_admin import credentials, db
import os
from config import FIREBASE_DB_URL

# Inicializa o Firebase apenas uma vez
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": FIREBASE_DB_URL
    })

# Função para salvar um token no Realtime Database
def salvar_dados_meme(token_data):
    ref = db.reference("/memecoins")
    ref.push(token_data)
    print(f"[FIREBASE] Token '{token_data['nome']}' salvo com sucesso.")
