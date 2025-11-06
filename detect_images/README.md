## Como clonar o repositório do Git

1.  Acesse o repositório no GitHub\
2.  Clique no botão verde **"Code"**\
3.  Copie a URL (HTTPS ou SSH)

### Executar o comando clone

git clone https://github.com/usuario/nome-do-repositorio.git

### Verificação pós-clone

Abra o terminal e execute: git status

**Passos resumidos:** 1. Copie a URL do repositório\
2. Abra o terminal na pasta desejada\
3. Execute:\
git clone URL_DO_REPOSITORIO\
4. Acesse a pasta:\
cd NOME_DO_REPOSITORIO\
5. Pronto! Você clonou o repositório 

------------------------------------------------------------------------

## Passo a passo do Django

1.  Verificar se o Python está instalado (instale se necessário)\
2.  Criar um ambiente virtual:\
    python -m venv myenv\
3.  Ativar o ambiente:\
    myenv`\Scripts`{=tex}`\activate  `{=tex}
4.  Instalar o Django:\
    pip install django\
5.  Verificar a instalação:\
    python -m django --version\
6.  Criar o projeto:\
    django-admin startproject meuprojeto\
    cd meuprojeto\
7.  Configurar o banco de dados:\
    python manage.py migrate\
8.  Criar superusuário:\
    python manage.py createsuperuser\
9.  Executar o servidor:\
    python manage.py runserver

------------------------------------------------------------------------

## Passo a passo do React

1.  Verificar instalação do Node.js:\
    node --version\
    npm --version\
2.  Instalar Node.js (se necessário): [nodejs.org](https://nodejs.org)\
3.  Criar aplicação React\
4.  Instalar dependências:\
    npm install\
    ou\
    yarn install\
5.  Executar a aplicação\
6.  Acessar a aplicação
