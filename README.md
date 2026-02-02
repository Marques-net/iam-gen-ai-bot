# IAM Gen AI Bot (MVP)

Plataforma multi-agentes para planejamento e produção de conteúdo (YouTube/Shorts/Instagram) com orquestração por estado, integração WhatsApp, cache e auditoria.

## Visão geral
- Orquestração com Supervisor e agentes especializados (SRP).
- Workspaces/campanhas isolados.
- Persistência em Postgres + cache Redis.
- Integrações plugáveis (LLM, busca web, WhatsApp).
- Revisão diária agendada + endpoints administrativos.

## Estrutura de pastas
```
/apps/api
/apps/worker
/core
/integrations
/infra
/docs
/tests
```

## Como rodar (Docker)
1. Copie `.env.example` para `.env` e ajuste variáveis conforme necessário.
2. Suba os serviços:
   ```bash
   docker compose -f infra/docker-compose.yml up --build
   ```
3. Rode as migrações:
   ```bash
   docker compose -f infra/docker-compose.yml exec api alembic -c infra/alembic.ini upgrade head
   ```
4. A API estará em `http://localhost:8000`.

## Endpoints principais (MVP)
- `GET /health`
- `POST /webhooks/whatsapp`
- `POST /workspaces/{workspace}/campaigns/{campaign}/generate-monthly`
- `GET /jobs/{job_id}`
- `POST /admin/run-daily-review`

## Configuração WhatsApp (MVP)
- O provedor é plugável via `WHATSAPP_PROVIDER`.
- Use o modo `mock` para simular mensagens no MVP.

## Comandos úteis
- Rodar lint: `ruff check .`
- Formatar: `black .`
- Testes: `pytest`

## Instruções Git (repositório local)
```bash
git init
git add .
git commit -m "chore: bootstrap repo"
# próximos commits conforme evolução do MVP
# tag final

git tag v0.1.0
```

## Notas de compliance
- Não utilizar conteúdo protegido sem licenciamento.
- Registrar fontes em pesquisas web.
- Respeitar COPPA e políticas do YouTube.
