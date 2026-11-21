# Análise de Filmes (TMDB) — `dados.ipynb`

Notebook de análise exploratória de um dataset de filmes do [TMDB](https://www.themoviedb.org/).

## Estrutura

```
.
├── dados.ipynb        # notebook principal
├── requirements.txt   # dependências
├── dados_limpeza_automatizada.ipynb # notebook à parte
├── dados_relevantes.ipynb    # gráficos utilizados na apresentação oral
├── filmes.json        # gerado ao executar (download ou coleta via API)
└── README.md
```

## Requisitos

- Python 3.10 ou superior (o notebook foi desenvolvido com Python 3.14)
- Conexão com a internet (download dos dados e instalação de pacotes)

## Instruções de execução

```bash
# 1. Clonar/baixar o projeto e entrar na pasta
cd <pasta-do-projeto>

# 2. Criar e ativar um ambiente virtual
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Abrir o notebook
jupyter lab dados.ipynb
```

Dentro do Jupyter, use **Run → Run All Cells** (ou *Kernel → Restart & Run All*). Execute as células em ordem: as colunas derivadas são criadas ao longo do notebook e as seções finais dependem delas.

O notebook também roda no Google Colab; nesse caso basta executar `!pip install gdown` na primeira célula.

### Dependências

| Pacote | Uso |
|---|---|
| `pandas`, `numpy` | manipulação dos dados |
| `matplotlib`, `seaborn` | gráficos |
| `gdown` | download automático do `filmes.json` (Google Drive) |
| `jupyterlab` | execução do notebook |

## Como obter os dados

O notebook espera o arquivo `filmes.json` (formato `records`, lido com `pd.read_json('filmes.json', orient='records')`).

### Opção A — Download automático (padrão)

A célula de importação já baixa o arquivo com `gdown` a partir do Google Drive e o salva como `filmes.json`. Nenhuma ação é necessária além de executar o notebook.

### Opção B — Coletar na API do TMDB

Use esta opção para reproduzir ou atualizar a base. **Requisito do dataset: apenas filmes com `budget > 0` e `revenue > 0`** (filmes sem orçamento ou receita informados são descartados, pois impossibilitam o cálculo de lucro e ROI).

1. Crie uma conta em <https://www.themoviedb.org/> e solicite uma chave de API em *Configurações → API*. Copie o **API Read Access Token** (Bearer).
2. Exporte o token e execute o script:

   ```bash
   export TMDB_TOKEN="seu_read_access_token"      # Windows (PowerShell): $env:TMDB_TOKEN="..."
   ```

3. O script gera `filmes.json` na pasta do projeto; basta pular (ou não executar) a célula do `gdown` no notebook.

**Como funciona a coleta**

- `GET /discover/movie` lista os IDs por ano de lançamento (a busca é fatiada por ano porque o TMDB limita o `discover` a 500 páginas por consulta).
- `GET /movie/{id}` traz os detalhes. O `budget` e o `revenue` só vêm nesse endpoint, e **não há filtro por eles no `discover`**; por isso o filtro `budget > 0 and revenue > 0` é aplicado depois, em Python.
- Os campos aninhados (`genres`, `production_companies`, `belongs_to_collection`) são mantidos como listas/dicionários, como o notebook espera.

> A coleta completa faz milhares de requisições e pode levar bastante tempo. O script espera e tenta de novo quando o TMDB devolve `429` (limite de requisições).

### Colunas usadas pelo notebook

`title`, `release_date`, `budget`, `revenue`, `profit`, `roi`, `popularity`, `vote_count`, `original_language`, `genres`, `production_companies`, `belongs_to_collection`.

O notebook descarta `backdrop_path`, `homepage`, `poster_path`, `status`, `adult` e `tagline`.

## Etapas de limpeza aplicadas no notebook

- Remoção de colunas sem utilidade analítica (listadas acima).
- Remoção de outliers: `roi <= 50000`, `budget > 1000` e `vote_count > 50`.
- Ajuste pela inflação com CPI histórico (base 2024) → `revenue_adj`, `budget_adj`, `profit_adj`.

## Atribuição

Este produto usa a API do TMDB, mas não é endossado nem certificado pelo TMDB. Consulte os [termos de uso da API](https://www.themoviedb.org/api-terms-of-use).