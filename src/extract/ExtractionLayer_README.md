# Extraction Layer — Conceptual Architecture and Contracts

## 0. Scope

This document defines the **conceptual architecture** of the Extraction Layer.  
No class is implemented yet — everything here represents **contracts, interfaces, and design intent**.  
The goal is to provide a **consistent, extensible, and environment-aware** data extraction framework driven by configuration.

---

## 1. Core Idea

The system converts **YAML-based configuration** into a series of **resolved, executable objects**.  
It separates configuration parsing, execution orchestration, and low-level strategy logic into independent layers.  
This makes the architecture **composable**, **testable**, and ready for both **batch** and **streaming** extraction.

### High-level flow

```
YAML → Loader → SourceSpec → ExtractorFactory (+ExecutionContext)
     → Extractor → Strategies → Landing Output
```

---

## 2. Folder and Module Structure

```
src/
  config/
    loader.py               # Parses YAML and produces validated SourceSpec objects.
    project.yaml            # Defines environments, profiles, defaults, datasets.
    README-contracts.md      # Technical index for the configuration contracts.

  extract/
    ExtractionLayer_README.md # This document.
    core/
      base.py                # Abstract base classes for extractors.
      context/
        execution_context.py  # Shared runtime metadata (env, tz, run_id, profiles).
      extractors/
        batch_extractor.py    # BatchExtractor contract.
        streaming_extractor.py# StreamingExtractor (conceptual).
        sources/ # Reserved for specialized source extractors if necessary
        
      factory.py              # ExtractorFactory: selects extractor class & injects strategies.
      models/
        plan_item.py          # Planned work unit before fetching.
        raw_response.py       # Raw payload returned by downloader.
        parsed_batch.py       # Validated structured batch ready for storage.
      policies/
        retry.py              # RetryPolicy.
        rate_limit.py          # Rate limiting behavior.
        idempotency.py        # Idempotent write control.
      registry.py             # Default class registry or mappings.
      resolvers/
        profile_resolver.py   # Resolves landing/silver/gold profiles by environment.
        secrets_resolver.py   # Expands secret placeholders.
      specs/
        dataset_spec.py       # Dataset-level metadata (schedule, format, access).
        source_spec.py        # BatchSourceSpec and future StreamingSourceSpec definitions.
      strategies/
        downloader/
          base.py             # DownloaderStrategy ABC.
          http_downloader.py
          file_downloader.py
          ftp_downloader.py
          db_downloader.py
        parsers/
          base.py             # ParserStrategy ABC.
          csv_parser.py
          json_parser.py
          parquet_parser.py
        storage_clients/
          base.py             # StorageClient ABC.
          fs_client.py
          s3_client.py
          db_client.py
      streaming/
        checkpoint_manager.py # Conceptual checkpoint tracker for stream mode.
        clients/
          kafka_client.py
          mqtt_client.py
          ws_client.py
    docs/
      architecture/           # Design notes, diagrams, and conceptual maps.
        01_specs_and_loader.md
        02_extractor_and_factory.md
        03_data_models.md
        execution_flow_diagram.md
        overview_map.md

  utils/
    config.py                 # Helper utilities for configuration handling.
    io_utils.py               # Common filesystem helpers.
```

---

## 3. Configuration Layer

### Loader
Parses the YAML configuration, validates it, and resolves profiles and secrets.  
Outputs a list of **SourceSpec** objects, ready for the factory.  
Performs no network or filesystem I/O.

**Responsibilities**
- Validate structure and required fields.
- Resolve `active_env` and profile mappings.
- Expand secrets using `SecretsResolver`.
- Return fully built `BatchSourceSpec` (or later `StreamingSourceSpec`).

### ProfileResolver
Translates logical profiles (landing/silver/gold) into resolved physical destinations.  
No I/O — computes only metadata.

### SecretsResolver
Expands environment variables or secure placeholders.  
Optional utility for injecting credentials dynamically.

---

## 4. Execution Layer

### ExtractorFactory
Entry point for execution; decides which extractor subclass to instantiate based on mode and source name.  
Injects `ExecutionContext` and appropriate strategy classes.  
Raises a clear error if no extractor fits the spec.

### BatchExtractor
Implements the full orchestration loop (Template Method pattern):

1. `prepare()`  
2. `plan()` → returns list of `PlanItem`
3. `fetch(plan_item)` → `RawResponse`
4. `parse(raw)` → `ParsedBatch`
5. `persist_landing(parsed)` → writes via `StorageClient`
6. `report()` → returns summary dictionary

Delegates all logic to strategies; performs no I/O itself.

### StreamingExtractor (conceptual)
Defines long-running ingestion for real-time data using `StreamingClient` and `CheckpointManager`.  
Not implemented yet.

---

## 5. Strategy Layer

### DownloaderStrategy
Retrieves raw data from external sources.  
Subclasses: `HttpDownloader`, `FileDownloader`, `FtpDownloader`, `DbDownloader`.

### ParserStrategy
Transforms raw payloads into structured data objects.  
Subclasses: `CsvParser`, `JsonParser`, `ParquetParser`.

### StorageClient
Writes parsed data to the landing/silver/gold layers, enforcing idempotency.  
Subclasses: `FsClient`, `S3Client`, `DbClient`.

### Streaming Components (future)
`StreamingClient` for brokers (`KafkaClient`, `MqttClient`, `WsClient`)  
and `CheckpointManager` for offset tracking.

---

## 6. Policy Layer

Encapsulates cross-cutting runtime rules:
- **RetryPolicy** — retry count and backoff behavior.  
- **RateLimitPolicy** — throttling rules for APIs or DBs.  
- **IdempotencyPolicy** — defines overwrite/deduplication semantics.

Policies can be injected into strategies or extractors.

---

## 7. Data Models

| Model | Description |
|-------|--------------|
| **PlanItem** | Single planned extraction unit; no I/O. |
| **RawResponse** | Encapsulates raw payload (bytes or stream) plus status/metadata. |
| **ParsedBatch** | Validated structured data ready to persist. |
| **LandingArtifact** | Conceptual note only — represents final stored artifact. |

---

## 8. Execution Context

Immutable object passed across all layers.  
Carries environment metadata such as timezone, profile roots, and run identifier.

**Fields**
- `env: str`
- `tz: str`
- `run_id: UUID`
- `logger`
- `profiles: dict[str, ResolvedProfile]`

---

## 9. Design Principles

- **Separation of Concerns** — clear division between configuration, orchestration, and I/O.  
- **Dependency Injection** — no hard-coded dependencies.  
- **Contract-Driven** — every class has an explicit purpose and interface.  
- **Extensibility** — add new connectors or formats by subclassing strategies.  
- **Environment Awareness** — everything resolved from YAML and profiles.  
- **Stateless Strategies** — only extractors hold control flow state.  
- **Streaming Parity** — streaming design mirrors batch.  
- **Policy-Based Behavior** — retry, throttling, idempotency all externalized.

---

## 10. Implementation Status

| Layer | Components | Status |
|--------|-------------|---------|
| **Configuration** | Loader, ProfileResolver, SecretsResolver, Specs | ✅ Defined |
| **Execution** | ExtractorFactory, BatchExtractor | ✅ Defined |
| **Streaming** | StreamingExtractor | 🕓 Conceptual |
| **Strategies** | Downloader, Parser, Storage | ✅ Defined |
| **Streaming Strategies** | StreamingClient, CheckpointManager | 🕓 Conceptual |
| **Policies** | Retry, RateLimit, Idempotency | ✅ Defined |
| **Models** | PlanItem, RawResponse, ParsedBatch | ✅ Defined |
| **Context** | ExecutionContext | ✅ Defined |

---

## 11. Summary

The **Extraction Layer** is fully specified at the conceptual level.  
It defines a modular, contract-driven design separating configuration, orchestration, and strategy logic.  
Batch mode is the immediate focus; streaming and advanced policies are designed for future implementation.  
This document serves as the authoritative blueprint for all upcoming code.
