import pyshark
import json
import os
from kafka import KafkaProducer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "pmacct_wifi")

print(f"Connecting to Kafka broker at {KAFKA_BROKER}")
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Open a live capture on mon0 (or from a pcap file if testing)
capture = pyshark.LiveCapture(interface='mon0')

print("Starting Wi-Fi packet parsing...")
for packet in capture.sniff_continuously():
    try:
        if 'WLAN' not in packet:
            continue

        # Only process data frames
        if int(packet.wlan.fc_type) != 2:
            continue

        src_mac = packet.wlan.sa if hasattr(packet.wlan, 'sa') else ''
        frame_len = int(packet.length)

        flow_record = {
            "mac_src": src_mac,
            "bytes": frame_len
        }

        print(f"Sending flow: {flow_record}")
        producer.send(KAFKA_TOPIC, flow_record)

    except Exception as e:
        print(f"Error processing packet: {e}")
