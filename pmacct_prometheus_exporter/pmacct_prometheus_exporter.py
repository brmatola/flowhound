import json
import os
import time
from kafka import KafkaConsumer
from prometheus_client import start_http_server, Gauge
from ip import get_direction
import threading

CONSUME_TOPICS = [
    ("pmacct_wired", "wired"),
    ("pmacct_wifi", "wifi"),
]

traffic_metric = Gauge(
    "pmacct_traffic_bytes_total",
    "Total bytes observed per flow",
    ["src_mac", "src_ip", "dst_ip", "direction", "source"]
)


def consume_topic(topic, source_label):
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "redpanda:9092")
    print(f"Connecting to Kafka broker at {KAFKA_BROKER}")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="pmacct_prometheus_exporter",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    print(f"Subscribed to Kafka topic {topic}")

    print(f"Consuming Kafka topic {topic}...")
    for message in consumer:
        data = message.value

        src_mac = data.get("mac_src", "")
        src_ip = data.get("ip_src", "")
        dst_ip = data.get("ip_dst", "")

        if not src_mac:
            continue

        direction = get_direction(src_ip, dst_ip)
        bytes = data.get("bytes", 0)

        print(f"Processing message: {topic} {direction} {src_mac} {bytes}")
        traffic_metric.labels(
            src_mac=src_mac,
            src_ip=src_ip,
            dst_ip=dst_ip,
            direction=direction,
            source=source_label,
        ).set(bytes)


if __name__ == "__main__":
    print("Starting Prometheus HTTP server on port 9105...")
    start_http_server(9105)

    print("Starting main")
    threads = []
    for topic, source_label in CONSUME_TOPICS:
        t = threading.Thread(
            target=consume_topic,
            args=(topic, source_label),
            daemon=True
        )
        t.start()
        threads.append(t)

    # Keep alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
