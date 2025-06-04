# Use Alpine for small size
FROM alpine:latest

# Install required tools
RUN apk add --no-cache iw bash

# Copy the hopper script
COPY hopper.sh /wifi_hopper.sh
RUN chmod +x /wifi_hopper.sh

# Run the hopper
CMD ["/wifi_hopper.sh"]
