# YottaFlex AI Data Pipeline Architecture

## Overview

The pipeline processes customer and order CSV files through ingestion, validation, transformation, publishing, and reconciliation stages.

## Architecture Flow


                 ┌────────────────────────┐
                 │ Synthetic Data Generator│
                 └────────────┬───────────┘
                              │
                   ┌──────────▼──────────┐
                   │   customers.csv    │
                   │     orders.csv     │
                   └──────────┬──────────┘
                              │
                   ┌──────────▼──────────┐
                   │     Ingestion      │
                   │ CSV + Schema Check │
                   └──────────┬──────────┘
                              │
                   ┌──────────▼──────────┐
                   │    Validation     │
                   │ Business Rules    │
                   └───────┬─────┬──────┘
                           │     │
                    Valid  │     │ Invalid
                           │     ▼
                           │  ┌──────────────┐
                           │  │ Reject Store │
                           │  └──────────────┘
                           ▼
                 ┌─────────────────────┐
                 │   Transformation   │
                 │ Customers / Orders │
                 │ Customer Summary   │
                 └──────────┬────────┘
                            │
                 ┌──────────▼──────────┐
                 │     Publishing     │
                 │   Parquet Files   │
                 └──────────┬─────────┘
                            │
                 ┌──────────▼──────────┐
                 │   Reconciliation   │
                 │ Counts + Amounts  │
                 └──────────┬─────────┘
                            │
                 ┌──────────▼──────────┐
                 │ Metrics & Reports  │
                 │ Run Status / JSON  │
                 └────────────────────┘


## Components

| Component | Responsibility |
|---|---|
| Generator | Reproducible synthetic datasets |
| Ingestion | CSV loading and schema validation |
| Validation | Business rules and data quality |
| Reject Handling | Invalid record tracking |
| Transformation | Standardization and aggregation |
| Publishing | Curated Parquet datasets |
| Reconciliation | Input/output consistency checks |
| Metrics | Run ID, status, duration, reports |
| Benchmark | Performance measurement |
| Tests | Automated correctness and reliability |