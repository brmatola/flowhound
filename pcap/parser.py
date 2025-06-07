import pyshark
import json
import os
import subprocess
import time
from kafka import KafkaProducer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "pmacct_wifi")

CHANNELS_24 = ["11"]
CHANNELS_5 = ["157"]
CHANNELS = CHANNELS_24 + CHANNELS_5
DWELL = 3 # seconds per channel
IFACE = "mon0"

print(f"Connecting to Kafka broker at {KAFKA_BROKER}")
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def set_channel(channel):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Switching {IFACE} to channel {channel}")
    try:
        subprocess.run(["iw", "dev", IFACE, "set", "channel", channel], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error switching channel: {e}")


while True:
    for channel in CHANNELS:
        set_channel(channel)

        capture = pyshark.LiveCapture(interface=IFACE)

        print(f"Listening on {IFACE} for {channel}...")

        try:
            capture.sniff(timeout=DWELL)
            for packet in capture:
                try:
                    if 'WLAN' not in packet:
                        continue

                    if int(packet.wlan.fc_type) != 2:
                        continue

                    src_mac = packet.wlan.sa if hasattr(packet.wlan, 'sa') else ''
                    frame_len = int(packet.length)

                    flow_record = {
                        "mac_src": src_mac,
                        "bytes": frame_len
                    }

                    print(f"Sending flow: {flow_record}")

                    print(f"Sending flow: {flow_record}")
                    producer.send(KAFKA_TOPIC, flow_record)
                except Exception as e:
                    print(f"Error processing packet: {e}")
        except Exception as e:
            print(f"Error processing capture: {e}")
        finally:
            capture.close()
