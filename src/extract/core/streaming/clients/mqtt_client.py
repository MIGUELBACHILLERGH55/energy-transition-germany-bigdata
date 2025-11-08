# src/extract/core/streaming/clients/mqtt_client.py

"""
MQTT Client
-----------

Implements StreamingClient for MQTT-based message brokers.

Responsibilities:
- Connect to MQTT broker with optional authentication.
- Subscribe to topics or channels defined in DatasetSpec.
- Stream incoming payloads as RawEvent objects.
- Handle reconnects and QoS levels gracefully.
- Integrate with CheckpointManager for delivery tracking.

Focused on lightweight IoT and telemetry data ingestion.
"""
