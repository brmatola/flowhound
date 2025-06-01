import json
import os
import time
from kafka import KafkaConsumer
from prometheus_client import start_http_server, Gauge

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = "pmacct_flows"

traffic_metric = Gauge(
    "pmacct_traffic_bytes_total",
    "Total bytes observed per flow",
    ["src_mac", "src_ip", "dst_ip"]
)


def main():
    print(f"Connecting to Kafka broker at {KAFKA_BROKER}")
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="pmacct_prometheus_exporter",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    print(f"Subscribed to Kafka topic {KAFKA_TOPIC}")

    print("Starting Prometheus HTTP server on port 9105...")
    start_http_server(9105)

    print(f"Consuming Kafka topic {KAFKA_TOPIC}...")
    for message in consumer:
        data = message.value
        if data.get("event_type") != "purge":
            continue

        src_mac = data.get("src_mac", "unknown")
        src_ip = data.get("ip_src", "unknown")
        dst_ip = data.get("ip_dst", "unknown")
        bytes = data.get("bytes", 0)

        traffic_metric.labels(
            src_mac=src_mac,
            src_ip=src_ip,
            dst_ip=dst_ip
        ).set(bytes)


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
