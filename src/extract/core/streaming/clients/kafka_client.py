# src/extract/core/streaming/clients/kafka_client.py

"""
Kafka Client
------------

Implements StreamingClient for Apache Kafka-based sources.

Responsibilities:
- Connect to Kafka brokers using configuration from SourceSpec.
- Subscribe to topics and consume messages in batches or streams.
- Handle offsets, partitions, and consumer group management.
- Expose an iterator of RawEvent objects for StreamingExtractor.
- Support checkpoint integration for reliable resume behavior.

This module defines connection and consumption logic — no parsing or persistence.
"""
