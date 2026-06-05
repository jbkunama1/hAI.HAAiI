# Security Policy

## Supported Versions

Only the latest version is actively maintained.

## Hardening Checklist

- [x] API key read exclusively from environment variable – never hardcoded
- [x] Internal endpoint auth via `HAI_INTERNAL_API_KEY` (`X-HAI-API-Key` header)
- [x] Input validation: role allow-list, max messages (50), max content length (8192)
- [x] Model allow-list via `HAI_ALLOWED_MODELS`
- [x] Rate limiting: 20 req/min per IP (slowapi)
- [x] TrustedHostMiddleware – restricts accepted `Host` headers
- [x] `follow_redirects=False` – no open redirect via OPENAI_BASE_URL
- [x] Upstream errors not leaked to client
- [x] Docker container runs as non-root user (`haiai`)
- [x] `.env` in `.gitignore` – secrets never committed
- [x] `/docs`, `/redoc`, `/openapi.json` disabled in production
- [x] Healthcheck endpoint at `/health`
- [x] Structured logging – no secrets in logs
- [x] Automated CVE scanning via GitHub Actions (Bandit, Safety, Trivy)
- [x] Dependabot enabled for pip + Docker

## Reporting a Vulnerability

Please open a **private** GitHub security advisory or contact the maintainer directly.
