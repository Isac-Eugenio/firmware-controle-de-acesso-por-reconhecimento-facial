
# 🔧 Firmware – Projeto Controle de Acesso por Reconhecimento Facial

## 📌 Introdução

Este repositório contém os **firmwares embarcados** utilizados no projeto principal:
👉 [backend-controle-de-acesso-por-reconhecimento-facial](https://github.com/Isac-Eugenio/backend-controle-de-acesso-por-reconhecimento-facial)

O sistema é composto por dois dispositivos ESP32 programados em C++, cada um com uma responsabilidade específica:

* 🎥 **ESP32-CAM** – responsável pela **captura de imagem** e envio dos dados para reconhecimento facial.
* 🔐 **ESP32-LOCK** – responsável pelo **acionamento de portas/trancas físicas** após a autenticação.

---

## 📦 Informações de Hardware

### ESP32-CAM

* **Modelo utilizado:** AI-THINKER
* **Função:** Captura de imagem facial para autenticação
* **Biblioteca base:**
  📚 [https://github.com/yoursunny/esp32cam](https://github.com/yoursunny/esp32cam) (créditos pela base da câmera)

### ESP32-LOCK

* **Modelo:** ESP32 genérico
* **Função:** Controle de travas, relés ou atuadores físicos após validação

---

## 🚀 Funcionalidades Integradas ao Sistema

Esses firmwares são parte de um sistema completo com backend em FastAPI. Juntos, permitem:

* 📸 Captura e envio de imagens faciais via ESP32-CAM
* 📡 Comunicação com API para envio de dados e validação
* 🔐 Controle de acesso físico via ESP32 (trancas, portas, sensores)
* ⚙️ Arquitetura desacoplada e escalável

---

