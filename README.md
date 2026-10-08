# Guia Completo: Git, GitHub e API TMDB

> Este guia foi feito para que todos no grupo consigam configurar o ambiente, trabalhar com Git/GitHub do zero e consumir os dados da API do TMDB.

---

## 1. Pré-requisitos (O que instalar antes)

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas na sua máquina:

1. **VS Code** (Editor de Código)
2. **Git**
   * **Windows:** Baixe no site oficial ([git-scm.com](https://git-scm.com/)) e instale com as opções padrão.
   * **Linux (Ubuntu/Debian):** Abra o terminal e execute:
     ```bash
     sudo apt update && sudo apt install git -y
     ```
3. **Python 3**
   * **Windows:** Baixe no site oficial ([python.org](https://www.python.org/)).  
     ⚠️ **MUITO IMPORTANTE:** Marque a caixinha **"Add Python to PATH"** durante a instalação.
   * **Linux:**
     ```bash
     sudo apt update && sudo apt install python3 python3-pip -y
     ```

---

## 💻 2. Instalando as Bibliotecas do Projeto

Abra o terminal integrado no VS Code (`Ctrl + '` ou `Ctrl + J`) na pasta do projeto e execute o comando correspondente ao seu sistema operacional:

### 🔹 No Windows:
```bash
pip install requests python-dotenv pandas
```

### 🔹 No Linux / macOS:
```bash
pip3 install requests python-dotenv pandas
```

> **O que cada biblioteca faz?**
> * `requests`: Faz as requisições para buscar dados de filmes diretamente na internet.
> * `python-dotenv`: Carrega a chave de API de forma segura a partir do arquivo `.env`.
> * `pandas`: Usada para criar tabelas (DataFrames) e analisar dados.

---

## 3. Configurando o Arquivo `.env` (Chave da API)

Para garantir a segurança, a chave da API **nunca deve ser enviada para o GitHub**. Ela é salva localmente no arquivo `.env`.

### O que você precisa fazer:
1. Baixe o arquivo `.env` que foi compartilhado no grupo privado (WhatsApp/Discord).
2. Mova ou cole esse arquivo **diretamente na raiz do projeto** (na mesma pasta onde ficam o `.gitignore` e os seus scripts `.py`).
3. Verifique se o conteúdo dele é parecido com isto:
   ```env
   TMDB_API_KEY=sua_chave_de_api_aqui
   ```

> 💡 **Se o Windows não deixar mover o arquivo ou mudar o nome:**
> Abra o VS Code, clique em **Novo Arquivo**, dê o nome de `.env` e cole o texto com a chave que o líder do grupo enviou.

---

## 4. Configuração Inicial do Git (Apenas na 1ª vez)

Apenas na primeira vez que for utilizar o Git no seu computador, abra o terminal e registre suas credenciais:

```bash
git config --global user.name "Seu Nome Completo"
git config --global user.email "seu-email@exemplo.com"
```

---

## 5. Entendendo Branches (Ramificações)

Pense no Git como um projeto estruturado em árvore:

* **`main` (ou `master`):** É o tronco principal do projeto, onde fica o código oficial e pronto. **Ninguém deve alterar a `main` diretamente!**
* **Branches (Ramificações):** São "cópias de trabalho" criadas para que cada integrante faça sua parte sem atrapalhar o código dos colegas.

### 📌 Regra de Ouro do Grupo:
> Para qualquer nova tarefa, crie uma **branch própria**.  
> Exemplo: `feature/grafico-generos`, `feature/conexao-api`, `fix/erro-nota`.

---

## 6. Fluxo de Trabalho Diário (Passo a Passo)

Siga este roteiro sempre que for trabalhar no projeto:

### Passo 1: Baixar as atualizações mais recentes
Antes de começar a programar, atualize seu repositório local com o que seus colegas fizeram:
```bash
git checkout main
git pull
```

### Passo 2: Criar e mudar para a sua nova branch
```bash
git checkout -b nome-da-sua-branch
```
*(Substitua por algo descritivo, ex: `git checkout -b feature/limpeza-dados`)*

### Passo 3: Escrever e testar seu código
Faça as alterações nos arquivos Python pelo VS Code e salve normalmente (`Ctrl + S`).

### Passo 4: Salvar suas alterações no Git (Commit)
1. Veja quais arquivos foram alterados:
   ```bash
   git status
   ```
2. Adicione os arquivos alterados para serem salvos:
   ```bash
   git add .
   ```
3. Crie um "ponto de salvamento" com uma mensagem clara do que foi feito:
   ```bash
   git commit -m "Adiciona script de filtragem por ano de lancamento"
   ```

### Passo 5: Enviar sua branch para o GitHub
Na primeira vez que for enviar uma nova branch para a nuvem:
```bash
git push -u origin nome-da-sua-branch
```
*(Nas próximas vezes dentro da mesma branch, basta digitar apenas `git push`)*

---

## 7. Código de Exemplo: Testando a API

ROde o arquivo `teste_api.py` para testar se a conexão e o arquivo `.env` estão funcionando corretamente. Isso aqui deve aparecer:

```text
{"success":true}
```

---

## 📌 Resumo Rápido de Comandos

| Comando | Para que serve? |
| :--- | :--- |
| `git status` | Mostra quais arquivos foram alterados ou criados. |
| `git checkout main` | Volta para a branch principal. |
| `git pull` | Baixa as alterações do GitHub para a sua máquina. |
| `git checkout -b minha-branch` | Cria e entra numa nova branch. |
| `git add .` | Prepara todos os arquivos modificados para o salvamento. |
| `git commit -m "mensagem"` | Salva uma versão com uma descrição do que foi feito. |
| `git push` | Envia suas commits/branches locais para o GitHub. |