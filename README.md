# Domain Knowledge RAG Platform

Local-first Retrieval-Augmented Generation platform for private domain knowledge. The planned system supports local open-weight models and optional commercial LLM providers behind a common interface.

## Project status

The repository structure and implementation plan are established. Application code will be delivered incrementally, beginning with a fully local end-to-end vertical slice.

## Repository layout

```text
apps/             Deployable API, worker, and web applications
packages/         Reusable domain modules
infrastructure/   Local and hosted deployment configuration
migrations/       Database schema migrations
tests/            Cross-application and acceptance tests
docs/             Architecture, decisions, and operating guides
scripts/          Developer and operational utilities
data/             Local runtime data; contents are not committed
outputs/          User-facing generated deliverables
work/             Temporary working files
```

See [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) for the delivery plan and [CONTRIBUTING.md](CONTRIBUTING.md) for repository conventions.

## Intended local services

- FastAPI API
- Background ingestion worker
- Next.js web application
- PostgreSQL with pgvector
- Redis
- vLLM serving Qwen3.5-35B-A3B GPTQ Int4
- Local filesystem document storage by default
- Optional MinIO profile

The target local startup command will be:

```bash
docker compose up --build
```

This command will be enabled once the Phase 1 service implementations and container definitions are added.

## Primary local model

The first supported local generation model is:

```text
Qwen/Qwen3.5-35B-A3B-GPTQ-Int4
```

The initial serving profile targets one NVIDIA RTX A6000 with 48 GB VRAM. It uses vLLM, text-only loading, GPTQ 4-bit MoE kernels, and a 32K operational context window. See [docs/LOCAL_MODEL.md](docs/LOCAL_MODEL.md) for the exact setup and validation procedure.
