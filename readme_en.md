# hAI.HAAiI – HomeAssistantAiInterface

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Addon-blue.svg)](#)
[![API](https://img.shields.io/badge/API-OpenAI%20compatible-purple.svg)](#)
[![Hardened](https://img.shields.io/badge/Security-Hardened-22c55e.svg)](SECURITY.md)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](#)

hAI.HAAiI is a modern, hardened OpenAI-compatible AI gateway for Home Assistant,
inspired by [ha-claude](https://github.com/Bobsilvio/ha-claude).

## Features
- OpenAI-compatible API (OpenAI, Ollama, local proxies, etc.)
- Input validation, rate limiting, internal auth out of the box
- Docker-ready: non-root user, healthcheck, Compose-ready
- Integrates into existing Docker Compose stacks (e.g. `highfishNetwork`)
- CI/CD security scanning via GitHub Actions (Bandit, Safety, Trivy)

## Quick Start
```bash
cp .env.example .env
# Edit .env – set OPENAI_API_KEY and OPENAI_BASE_URL
docker compose up -d
```

## Configuration
| Variable | Description | Required |
|---|---|---|
| `OPENAI_API_KEY` | Your API key | Yes |
| `OPENAI_BASE_URL` | API base URL | Recommended |
| `OPENAI_MODEL` | Default model | Optional |
| `HAI_INTERNAL_API_KEY` | Protects the endpoint | Recommended |
| `HAI_ALLOWED_MODELS` | Comma-separated model allow-list | Optional |
| `HAI_ALLOWED_HOSTS` | Trusted Host header values | Recommended |

## Home Assistant Integration
Point the built-in OpenAI conversation integration or a `rest_command` at `http://hai-haaii:8787`.

## License
MIT – see [LICENSE](LICENSE).
