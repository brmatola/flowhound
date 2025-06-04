#!/bin/bash

set -e

# Interface to hop
IFACE="mon0"

# Channels to hop — adjust as needed!
CHANNELS_24="11"
CHANNELS_5="157"

# Combined — you can tune this later
CHANNELS="$CHANNELS_24 $CHANNELS_5"

# Dwell time per channel (seconds)
DWELL=3

echo "Starting Wi-Fi hopper on $IFACE"
while true; do
    for CH in $CHANNELS; do
        echo "[$(date)] Switching $IFACE to channel $CH"
        iw dev $IFACE set channel $CH
        sleep $DWELL
    done
done
