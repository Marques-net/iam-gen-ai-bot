# Arquitetura (MVP)

## Fluxo principal (Mermaid)
```mermaid
sequenceDiagram
    participant WA as WhatsApp
    participant Intake as IntakeAgent
    participant Sup as SupervisorAgent
    participant Research as ResearchAgent
    participant Idea as IdeationAgent
    participant Sched as SchedulerAgent
    participant Script as ScriptWriterAgent
    participant Story as StoryboardAgent
    participant Edit as EditorGuideAgent
    participant DB as Postgres/Redis

    WA->>Intake: mensagem + parâmetros
    Intake->>Sup: parâmetros validados / pendências
    Sup->>DB: carregar workspace/campanha
    Sup->>Research: pesquisa tendências
    Research->>DB: salvar fontes + cache
    Sup->>Idea: gerar ideias
    Idea->>DB: salvar ideias
    Sup->>Sched: montar agenda mensal
    Sched->>DB: salvar calendário
    Sup->>Script: gerar roteiros (amostra)
    Sup->>Story: gerar storyboards
    Sup->>Edit: gerar guias de edição
    Sup->>WA: solicitar aprovação
```

## Componentes
- **API (FastAPI)**: webhooks, comandos e gatilhos de geração.
- **Worker**: scheduler diário para revisão.
- **Core**: agentes, estado do workflow, memória e orquestração.
- **Integrations**: provedores pluggáveis de LLM, busca web e WhatsApp.
- **Infra**: Docker Compose + Alembic migrations.
