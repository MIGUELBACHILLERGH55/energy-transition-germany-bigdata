# src/extract/core/streaming/clients/ws_client.py

"""
WebSocket Client
----------------

Implements StreamingClient for WebSocket-based real-time APIs.

Responsibilities:
- Establish and maintain a persistent WebSocket connection.
- Receive and yield messages as RawEvent objects.
- Manage reconnections and heartbeat signals.
- Handle authentication or token renewal when required.
- Integrate with CheckpointManager for event continuity.

Used for push-based or event-driven data sources.
"""
