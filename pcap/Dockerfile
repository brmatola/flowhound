FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tshark \
    iw \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY parser.py .

CMD ["python", "parser.py"]