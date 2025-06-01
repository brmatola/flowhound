FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pmacct_prometheus_exporter.py .

CMD ["python", "pmacct_prometheus_exporter.py"]