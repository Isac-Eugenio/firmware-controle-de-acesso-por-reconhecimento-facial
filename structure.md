# 📁 Estrutura do Projeto

Este documento descreve a função de cada diretório e arquivo no projeto.

## Diretórios

- **controllers/**  
  Camada que define os controladores da API (ex: rotas e endpoints FastAPI).

- **core/**  
  Contém configurações centrais (ex: configurações de app, exceções personalizadas, autenticação).

- **models/**  
  Modelos de dados (Pydantic), incluindo entrada e saída de dados, DTOs, etc.

- **repository/**  
  Implementa o acesso ao banco de dados. Define os repositórios com lógica de persistência.

- **services/**  
  Camada de serviço responsável pela lógica de negócio. Orquestra controllers e repositórios.

- **__pycache__/**  
  Diretório automático do Python para armazenar arquivos compilados (`.pyc`).

- **.build/**  
  Scripts e artefatos de build, incluindo `build.sh`.

## Arquivos

- **main.py**  
  Arquivo principal que inicia o servidor FastAPI e configura as rotas.

- **docker-compose.yml**  
  Define os serviços de container para rodar o projeto (ex: banco de dados, API, etc).

- **requirements.txt**  
  Lista de dependências Python do projeto.

- **install.sh**  
  Script de instalação automatizada (ambiente local).

- **tests.py**  
  Contém testes unitários ou de integração para os componentes da aplicação.

- **readme.md**  
  Visão geral do projeto, instruções de uso e configuração.

- **.gitignore / .dockerignore**  
  Arquivos e pastas ignoradas pelo Git e Docker durante versionamento/build.

