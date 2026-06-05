# hAI.HAAiI – HomeAssistantAiInterface

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Addon-blue.svg)](#)
[![API](https://img.shields.io/badge/API-OpenAI%20compatible-purple.svg)](#)
[![Hardened](https://img.shields.io/badge/Hardened-Security%20checked-22c55e.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](#)

hAI.HAAiI ist eine moderne, OpenAI-kompatible Schnittstelle für Home Assistant,
inspiriert von [ha-claude](https://github.com/Bobsilvio/ha-claude), aber optimiert
für Docker-Deployments und ein „API-Key rein, los geht’s“-Setup.

## Features

- OpenAI-kompatible API (OpenAI, Ollama, lokale Proxys, etc.)
- Einfache Konfiguration via Umgebungsvariablen oder `.env`
- Interner API-Key-Schutz (`HAI_INTERNAL_API_KEY`)
- Input-Validierung, Rate Limiting, strukturiertes Logging
- Healthcheck-Endpoint `/health`
- Läuft als Home Assistant Add-on oder separater Docker-Container

## Architektur

- Backend: FastAPI (Python 3.11+)
- Schnittstelle: `POST /v1/chat/completions` (OpenAI-kompatibel)
- Optional: Modell-Allow-List, TrustedHostMiddleware

## Installation

```bash
git clone https://github.com/jbkunama1/hAI.HAAiI.git
cd hAI.HAAiI
cp .env.example .env
# .env bearbeiten: OPENAI_API_KEY, OPENAI_BASE_URL etc. setzen
docker compose up -d
```

## Konfiguration

| Variable | Beschreibung | Pflicht |
|---|---|---|
| `OPENAI_API_KEY` | API-Key für Upstream | ✅ |
| `OPENAI_BASE_URL` | Upstream-URL | empfohlen |
| `OPENAI_MODEL` | Standardmodell | optional |
| `HAI_INTERNAL_API_KEY` | Endpoint-Absicherung | empfohlen |
| `HAI_ALLOWED_MODELS` | Modell-Allow-List (Komma-sep.) | optional |
| `HAI_ALLOWED_HOSTS` | Erlaubte Host-Header | empfohlen |

## Nutzung mit Home Assistant

Über `rest_command`, Assist oder eigene Integrationen – der Service lauscht auf Port `8787`.

Typische Use-Cases:
- Natürliche Sprache für Automationen
- AI-Assistent mit Zugriff auf HA-Daten
- AI-basierte Benachrichtigungen und Log-Analyse

## Entwicklung

```bash
pip install -r requirements.txt
uvicorn hai_haaii.main:app --reload --port 8787
```

## Lizenz

MIT – siehe [LICENSE](LICENSE).
