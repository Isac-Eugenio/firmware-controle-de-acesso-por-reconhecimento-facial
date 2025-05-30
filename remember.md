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



# 📌 Convenção de Nomenclatura para Commits e Pull Requests

Este documento define as nomenclaturas e prefixos recomendados para padronizar os commits e pull requests neste repositório.

---

## ✅ Prefixos para Mensagens de Commit e Títulos de Pull Requests

| Prefixo       | Uso Principal                                              | Exemplo                                                  |
|---------------|------------------------------------------------------------|-----------------------------------------------------------|
| `feat:`       | Nova funcionalidade                                        | `feat: adicionar sistema de login com JWT`               |
| `fix:`        | Correção de bug                                            | `fix: corrigir erro na validação do email`               |
| `docs:`       | Documentação (README, comentários, etc.)                   | `docs: atualizar instruções de instalação`               |
| `style:`      | Formatação, identação, espaços em branco                   | `style: aplicar padrão Prettier nos arquivos js`         |
| `refactor:`   | Refatoração de código (sem mudança de comportamento)       | `refactor: simplificar lógica de autenticação`           |
| `perf:`       | Melhorias de performance                                   | `perf: otimizar carregamento de dados na dashboard`      |
| `test:`       | Adição ou alteração de testes                              | `test: adicionar testes unitários ao componente Header`  |
| `chore:`      | Tarefas de manutenção do projeto                           | `chore: atualizar dependências do projeto`               |
| `ci:`         | Configuração ou ajustes na integração contínua             | `ci: corrigir pipeline do GitHub Actions`                |

---

## 🚧 Prefixos para Estágio de Desenvolvimento

| Prefixo/Tag       | Quando usar                                       | Exemplo                                               |
|-------------------|---------------------------------------------------|--------------------------------------------------------|
| `wip:`            | Work in progress (trabalho em andamento)         | `wip: implementação inicial da página de perfil`      |
| `ready:`          | Tarefa/PR pronta para revisão ou merge           | `ready: módulo de relatórios finalizado`              |
| `done:`           | Etapa concluída com sucesso                      | `done: finalização da etapa 2 do sistema`             |
| `complete:`       | Entrega completa de uma funcionalidade           | `complete: dashboard administrativa`                  |
| `final:`          | Finalização de uma versão ou funcionalidade      | `final: ajustes finais no layout responsivo`          |
| `milestone:`      | Entregas importantes (MVP, Beta, etc.)           | `milestone: MVP concluído`                            |

---

## 📎 Labels (Tags) recomendadas para Pull Requests

> Use-as como etiquetas visuais nas PRs para indicar status e tipo.

- `type:feature`
- `type:bugfix`
- `type:refactor`
- `type:documentation`
- `status:wip`
- `status:review`
- `status:done`
- `priority:high`
- `stage:testing`
- `milestone:<nome>` (ex: `milestone: Sprint 3`, `milestone: MVP`)

---

## 🧪 Boas Práticas

- Use títulos curtos e objetivos.
- Detalhe as mudanças no corpo da Pull Request.
- Utilize `closes #issue` para vincular a uma issue automaticamente.
- Marque os revisores quando necessário.
- Teste antes de enviar a PR.

---

## 📘 Exemplo de título de PR

- feat(auth): adicionar autenticação com Google OAuth

## 📘 Exemplo de mensagem de commit

fix: corrigir bug ao carregar usuários no painel admin


> Mantenha este padrão para facilitar a colaboração, revisão e rastreamento de alterações no projeto.