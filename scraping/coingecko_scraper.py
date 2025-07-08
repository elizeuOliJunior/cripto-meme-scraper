import requests
from datetime import datetime

def coletar_memecoins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "category": "meme-token",
        "order": "market_cap_desc"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        resultado = []

        for coin in data:
            resultado.append({
                "nome": coin["name"],
                "preco_usd": coin["current_price"],
                "volume_24h": coin["total_volume"],
                "fonte": "CoinGecko",
                "timestamp": datetime.utcnow().isoformat()
            })

        return resultado

    except Exception as e:
        print(f"[ERRO] Falha ao coletar dados da CoinGecko: {e}")
        return []
