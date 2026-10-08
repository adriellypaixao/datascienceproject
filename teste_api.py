import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente salvas no arquivo .env
load_dotenv()

# Recupe a chave armazenada
api_key = os.getenv("TMDB_API_KEY")

url = "https://api.themoviedb.org/3/authentication"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

print(response.text)