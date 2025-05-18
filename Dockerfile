FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sma_mqtt/ sma_mqtt/

CMD ["python", "-m", "sma_mqtt.main"]
