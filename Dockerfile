FROM python:3.14-slim

RUN useradd --create-home --no-log-init haiai

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY hai_haaii/ ./hai_haaii/

USER haiai
EXPOSE 8787

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8787/health')"

CMD ["uvicorn", "hai_haaii.main:app", "--host", "0.0.0.0", "--port", "8787", "--no-access-log"]
