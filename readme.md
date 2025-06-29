
# Backend Projeto Controle de Acesso por Reconhecimento Facial

## 📌 Introdução

O Backend do Projeto Controle de Acesso por Reconhecimento Facial é a base de um sistema inteligente de autenticação que utiliza visão computacional e biometria facial para controlar e autorizar o acesso de usuários em ambientes físicos ou digitais. Desenvolvido em Python, este backend é estruturado com foco em modularidade, desempenho assíncrono e segurança.

Ele integra tecnologias como FastAPI, OpenCV, face_recognition e MySQL, permitindo o registro, autenticação e gerenciamento de usuários com base em reconhecimento facial. A API pode ser consumida por painéis web, aplicações móveis ou dispositivos embarcados.

### 🔧 Funcionalidades Principais

* 📸 Cadastro de usuários com base em imagens faciais

* 🧠 Reconhecimento facial por vetores de similaridade

* 🔐 Validação de acesso por ID e credenciais

* 🗂️ CRUD completo para usuários (criar, listar, atualizar, excluir)

* 🧪 Sistema de testes automatizados para endpoints e regras

* ⚙️ Arquitetura desacoplada (controllers, services, models e repositórios)

* 📡 API assíncrona e escalável baseada em FastAPI

* 💾 Persistência com banco de dados relacional (MySQL)

* 🔌 Comunicação direta com sistemas  embarcados como Arduino ou ESP32, permitindo controle físico de portas, travas e sensores

---

## 🚀 Instalação

### ✅ Requisitos

* 🐧 **Sistema operacional:** baseado em **Debian Linux** (recomendado: [DietPi](https://dietpi.com))
* ⚙️ **Arquitetura suportada:** ARM64 ou x64
* 📡 **Hardware obrigatório:** pelo menos um **ESP32** e um **ESP32-CAM**
* 🐳 **Docker e Docker Compose instalados**

  * 📦 [Instalar Docker](https://docs.docker.com/engine/install/ubuntu/)
  * 📦 [Instalar Docker Compose](https://docs.docker.com/compose/install/)

---

### 🛠️ Pré-instalação

Antes de iniciar o backend, você deve configurar o firmware dos dispositivos embarcados:

👉 Repositório do firmware:
**[firmware-controle-de-acesso-por-reconhecimento-facial](https://github.com/Isac-Eugenio/firmware-controle-de-acesso-por-reconhecimento-facial)**

Siga o tutorial do repositório acima para instalar o firmware no **ESP32** e no **ESP32-CAM** usados neste projeto.

---

### 📥 Passo a passo para instalar o backend

#### 1. Clone o repositório:

```bash
git clone https://github.com/Isac-Eugenio/backend_controle_de_acesso.git
```

#### 2. Acesse a pasta do projeto:

```bash
cd backend_controle_de_acesso
```

#### 3. Configure os arquivos:

##### 🛠️ Arquivo de configuração da aplicação:

Edite o arquivo `core/config/config.yaml` com suas variáveis personalizadas:

```bash
sudo nano core/config/config.yaml
```

Configure:

* Conexão com o banco de dados (host, porta, usuário, senha, nome)
* Nome do projeto, permissões de usuário, etc.

##### 🐳 Arquivo `docker-compose.yml`:

Edite o `docker-compose.yml` e **garanta que os valores (como `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`) estejam sincronizados com o `config.yaml`**:

```bash
sudo nano docker-compose.yml
```

> 🔁 **Atenção:** Os dados de conexão devem ser consistentes entre `config.yaml` e `docker-compose.yml` para que o backend consiga acessar o banco MySQL corretamente.

---

#### 4. Execute o script de instalação:

```bash
sudo chmod +x install.sh
source install.sh
```

Esse script realiza a instalação das dependências necessárias para o funcionamento do backend.

---

#### 5. Inicie o servidor com o script de inicialização:

```bash
chmod +x start.sh
./start.sh
```

Esse script irá:

* ✅ Verificar se o `uvicorn` está instalado e instalar, se necessário
* 🚀 Iniciar a API FastAPI em `0.0.0.0:5050`

---

### ✅ Acesso à API:

* Localmente: [http://localhost:5050](http://localhost:5050)
* Em rede: `http://<IP_DO_SERVIDOR>:5050`

> 🔒 Certifique-se de que a porta `5050` está liberada no firewall ou roteador se quiser acesso externo.

---
