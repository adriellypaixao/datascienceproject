import os
import json
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TMDB_API_KEY")
if not token:
    raise SystemExit("TMDB_API_KEY não encontrada no .env")

BASE = "https://api.themoviedb.org/3"

# ---- Configurações ----
ANO_INICIO = 2005
ANO_FIM = 2025          # ano corrente (2026) ainda está incompleto
MAX_POR_ANO = 500       # limite de filmes por ano
MIN_VOTOS = 50         # evita notas baseadas em poucos votos
PASTA = "data"
# -----------------------

os.makedirs(PASTA, exist_ok=True)
ARQ_IDS = f"{PASTA}/ids.json"
ARQ_JSONL = f"{PASTA}/filmes_bruto.jsonl"
ARQ_CSV = f"{PASTA}/filmes_bruto.csv"

session = requests.Session()
session.headers.update({
    "accept": "application/json",
    "Authorization": f"Bearer {token}",
})


def get_json(url, params=None, tentativas=3):
    for tentativa in range(1, tentativas + 1):
        try:
            r = session.get(url, params=params, timeout=15)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", 2)))
            else:
                print(f"HTTP {r.status_code} em {url}")
                if r.status_code in (401, 404):
                    return None
        except requests.RequestException as e:
            print(f"Erro de rede ({e}), tentativa {tentativa}/{tentativas}")
            time.sleep(1)
    return None


# 1) IDs por ano via discover (pula se já foi feito)
if os.path.exists(ARQ_IDS):
    with open(ARQ_IDS, encoding="utf-8") as f:
        movie_ids = json.load(f)
    print(f"{len(movie_ids)} IDs carregados de {ARQ_IDS}")
else:
    todos = {}
    for ano in range(ANO_INICIO, ANO_FIM + 1):
        do_ano = set()
        page = 1
        while len(do_ano) < MAX_POR_ANO and page <= 500:
            dados = get_json(f"{BASE}/discover/movie", params={
                "language": "pt-BR",
                "include_adult": "false",
                "sort_by": "popularity.desc",
                "primary_release_date.gte": f"{ano}-01-01",
                "primary_release_date.lte": f"{ano}-12-31",
                "vote_count.gte": MIN_VOTOS,
                "with_runtime.gte": 60,   # exclui curtas
                "page": page,
            })
            if not dados:
                break
            for filme in dados.get("results", []):
                if len(do_ano) < MAX_POR_ANO:
                    do_ano.add(filme["id"])
            if page >= dados.get("total_pages", 0):
                break
            page += 1
            time.sleep(0.05)
        print(f"{ano}: {len(do_ano)} filmes")
        for i in do_ano:
            todos[i] = ano

    movie_ids = list(todos)
    with open(ARQ_IDS, "w", encoding="utf-8") as f:
        json.dump(movie_ids, f)
    print(f"Total de filmes únicos: {len(movie_ids)}")

# 2) Detalhes, gravando linha a linha (retomável)
ja_baixados = set()
if os.path.exists(ARQ_JSONL):
    with open(ARQ_JSONL, encoding="utf-8") as f:
        for linha in f:
            try:
                ja_baixados.add(json.loads(linha)["id"])
            except (json.JSONDecodeError, KeyError):
                pass

pendentes = [i for i in movie_ids if i not in ja_baixados]
print(f"{len(ja_baixados)} já baixados, {len(pendentes)} pendentes")

falhas = []
with open(ARQ_JSONL, "a", encoding="utf-8") as f:
    for idx, movie_id in enumerate(pendentes, start=1):
        detalhe = get_json(f"{BASE}/movie/{movie_id}", params={
            "language": "pt-BR",
            "append_to_response": "credits",   # elenco e equipe na mesma chamada
        })
        if detalhe:
            f.write(json.dumps(detalhe, ensure_ascii=False) + "\n")
            f.flush()
        else:
            falhas.append(movie_id)

        if idx % 100 == 0:
            print(f"{idx}/{len(pendentes)} processados...")
        time.sleep(0.05)

if falhas:
    print(f"Atenção: {len(falhas)} falharam. Rode de novo para tentar outra vez.")

# 3) Converte o JSONL em CSV
with open(ARQ_JSONL, encoding="utf-8") as f:
    registros = [json.loads(linha) for linha in f if linha.strip()]

df = pd.DataFrame(registros).drop_duplicates(subset="id")
for col in df.columns:
    if df[col].map(lambda v: isinstance(v, (list, dict))).any():
        df[col] = df[col].map(
            lambda v: json.dumps(v, ensure_ascii=False)
            if isinstance(v, (list, dict)) else v
        )

df.to_csv(ARQ_CSV, index=False, encoding="utf-8")
print(f"\nPronto! {ARQ_CSV} com {len(df)} filmes.")