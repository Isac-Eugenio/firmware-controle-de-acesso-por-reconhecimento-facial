# 🧠 Diferença entre Model, Repository, Service, Controller e Utils

Na arquitetura de software, especialmente em projetos organizados com camadas (como MVC ou Clean Architecture), cada classe tem uma **responsabilidade bem definida**. Entender a função de cada uma ajuda a manter o código limpo, reutilizável e fácil de manter.

---

## 🔍 Tabela Comparativa

| Camada        | Responsabilidade Principal                                             | Exemplo no contexto de reconhecimento facial                              |
|---------------|------------------------------------------------------------------------|---------------------------------------------------------------------------|
| **Model**     | Representa **dados** da aplicação. Geralmente usado para armazenar, transferir ou persistir informações. | `FaceModel` com atributos como `id`, `nome`, `encoding`, `localização`.   |
| **Repository**| Responsável por **acessar fontes de dados externas**, como banco de dados, arquivos ou dispositivos. | `FaceRepository` que salva e carrega encodings do banco ou arquivo.      |
| **Service**   | Contém a **lógica de negócio**. Usa os Models e Repositories para aplicar regras do sistema. | `FaceService` que valida rostos, autoriza entrada, etc.                  |
| **Controller**| Controla o **fluxo da aplicação**. Recebe comandos (do usuário ou do sistema), coordena Services e decide o que fazer. | `FaceController` que recebe o frame e inicia o processo de validação.    |
| **Utils**     | Classes auxiliares que **fornecem funcionalidades específicas**. Não controlam fluxo nem contêm regra de negócio. | `FaceUtils` que calcula localização e encodings usando `face_recognition`. |

---

## 📌 Resumo rápido:
- **Model** → dados  
- **Repository** → acesso a dados externos  
- **Service** → lógica do sistema  
- **Controller** → orquestra tudo  
- **Utils** → ferramentas auxiliares

---

> **Exemplo:** no seu projeto de reconhecimento facial, a `FaceUtils` **não é um Model**, pois ela **processa dados temporários**.  
> Ela seria melhor classificada como um **Service** (se aplicar regras) ou **Utils** (se apenas fornecer funções).
