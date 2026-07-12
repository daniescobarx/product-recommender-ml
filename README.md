# ecommerce-recommender-system

Sistema de recomendacao de produtos para e-commerce desenvolvido em etapas para o
Tech Challenge de pos-graduacao. A base atual preserva a estrutura em `src/`,
testes automatizados, Ruff, pre-commit e componentes iniciais de preprocessamento
e modelos baseline.

## Etapa 2: Ambiente e Dependencias

Esta etapa prepara um ambiente reproduzivel para desenvolvimento local, testes e
proximas fases do projeto. O foco esta em Poetry, lock file, configuracao externa
via `.env` e validacao automatizada do ambiente.

### Decisoes tecnicas

- **Poetry** gerencia dependencias, empacotamento e instalacao limpa do projeto.
- **Python `>=3.11,<3.13`** evita versoes antigas e reduz risco de incompatibilidade
  com bibliotecas de ML.
- **Pydantic Settings** centraliza configuracoes externas com validacao forte.
- **Logging padrao** sera usado inicialmente. A dependencia `loguru` nao foi
  adicionada para evitar acoplamento desnecessario; o `logging` da biblioteca
  padrao e suficiente para a Etapa 2.
- **MLflow e DVC** ficam no grupo opcional `mlops`. Assim, entram no
  `poetry.lock` quando o lock e gerado, mas nao pesam na instalacao basica da
  Etapa 2. Instale com `--with mlops` apenas quando iniciar tracking, versionamento
  de dados ou pipelines nas proximas etapas.

### Dependencias principais

- `torch`: base para os modelos neurais de recomendacao das proximas etapas.
- `scikit-learn`: metricas, validacao, preprocessamento e baselines classicos.
- `pandas`: manipulacao tabular de catalogo, usuarios, itens e interacoes.
- `numpy`: computacao numerica usada por pandas, scikit-learn e features.
- `pydantic`: validacao tipada de objetos e configuracoes.
- `pydantic-settings`: carregamento de configuracoes por variaveis de ambiente.
- `python-dotenv`: suporte ao arquivo `.env` em desenvolvimento local.
- `typer`: base simples para futuros comandos CLI sem criar framework proprio.

### Dependencias de desenvolvimento

- `pytest`: execucao dos testes automatizados.
- `pytest-cov`: relatorio de cobertura quando necessario.
- `ruff`: lint e formatacao rapidos em uma unica ferramenta.
- `pre-commit`: execucao automatica de checks antes de commits.
- `mypy`: checagem estatica para manter contratos tipados.
- `pandas-stubs`: melhora a analise de tipos em codigo que usa pandas.

### Pre-requisitos

- Python 3.11 ou 3.12 disponivel no terminal.
- Poetry instalado.
- Git disponivel no terminal.

Instalacao recomendada do Poetry:

```bash
python -m pip install --user pipx
python -m pipx ensurepath
pipx install poetry
```

Em algumas instalacoes Linux/WSL, o comando pode ser `python3`:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install poetry
```

Valide a instalacao:

```bash
poetry --version
```

### Instalacao do projeto

Clone o repositorio e entre na raiz do projeto:

```bash
git clone <repository-url>
cd ecommerce-recommender-system
```

Instale o ambiente basico:

```bash
poetry install
```

Para instalar tambem as dependencias opcionais de MLOps:

```bash
poetry install --with mlops
```

### Arquivo .env

Crie o `.env` local a partir do exemplo versionado:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

O arquivo `.env` real nao deve ser commitado. Use apenas valores locais e nunca
adicione segredos ao repositorio.

Variaveis suportadas:

```env
APP_NAME=ecommerce-recommender-system
ENVIRONMENT=local
RANDOM_SEED=42
DATA_DIR=data
RAW_DATA_DIR=data/raw
PROCESSED_DATA_DIR=data/processed
MODEL_DIR=models
ARTIFACTS_DIR=artifacts
LOG_LEVEL=INFO
MLFLOW_TRACKING_URI=./mlruns
MLFLOW_EXPERIMENT_NAME=ecommerce-recommender-local
```

### Lock file

O `poetry.lock` registra as versoes exatas resolvidas para dependencias diretas
e transientes. Ele deve ser commitado para que outra pessoa consiga reconstruir
o mesmo ambiente com `poetry install`.

Gere ou atualize o lock file:

```bash
poetry lock
```

Depois instale a partir do lock:

```bash
poetry install
```

### Validacao do ambiente

Execute:

```bash
poetry check
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest
poetry run python scripts/validate_env.py
poetry run pre-commit run --all-files
```

O script `scripts/validate_env.py` verifica versao do Python, imports das
dependencias principais, import do package `recommender_system`, carregamento das
settings e disponibilidade dos diretorios esperados.

### Problemas comuns

- **`poetry: command not found`**: instale o Poetry com `pipx` e reabra o terminal.
- **Versao errada do Python**: configure o interpretador com
  `poetry env use python3.11` ou `poetry env use python3.12`.
- **Falha ao instalar `torch`**: confirme que o Python usado pelo Poetry esta
  dentro do intervalo suportado e que ha conexao com o indice de pacotes.
- **`ModuleNotFoundError: recommender_system`**: rode os comandos pela raiz do
  projeto e execute `poetry install` novamente.
- **Pre-commit falhando por formatacao**: rode `poetry run ruff format .` e depois
  repita `poetry run pre-commit run --all-files`.

## Comandos finais da Etapa 2

```bash
poetry install
poetry check
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest
poetry run python scripts/validate_env.py
poetry run pre-commit run --all-files
```
