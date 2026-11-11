FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app.py frontend.py start.sh ./
COPY model/ ./model/
COPY schema/ ./schema/
COPY config/ ./config/

# Fix Windows line endings (CRLF) so the script runs on Linux, then make it executable
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=3); urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)" || exit 1

CMD ["./start.sh"]