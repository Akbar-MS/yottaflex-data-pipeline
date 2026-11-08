# YottaFlex AI – Data Engineering Challenge

## Scalable Batch Data Processing Pipeline

A production-inspired batch data pipeline built using Python, Pandas, and Apache Parquet. The pipeline ingests customer and order datasets, validates records, transforms data into curated datasets, and publishes outputs with reconciliation, observability, and failure-recovery capabilities.

## 1. Project Overview

This project demonstrates a reliable batch processing workflow designed for data quality, reproducibility, and operational transparency.

### Key Features
- CSV ingestion with schema validation
- Customer and order data validation
- Duplicate and null key detection
- Business-rule validation
- Malformed record quarantine
- Customer and order transformations
- Customer-level order aggregation
- Parquet-based curated datasets
- Centralized reject tracking
- Run metrics and execution reports
- Input-to-output reconciliation
- Idempotent publishing
- Automated testing using pytest
- Synthetic data generation at scale
- Performance benchmarking

## 2. Architecture

```text
Synthetic CSV Data
       |
       v
    Ingestion
       |
       v
 Schema Validation
       |
       v
 Business Validation
       |
       +------> Reject Records
       |
       v
 Transformation
       |
       +------> Curated Customers
       |
       +------> Curated Orders
       |
       +------> Customer Order Summary
       |
       v
 Parquet Publishing
       |
       v
 Reconciliation
       |
       v
 Run Metrics & Reports
```

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline implementation |
| Pandas | Data processing and transformations |
| PyArrow | Parquet storage |
| pytest | Automated testing |
| PyYAML | Configuration support |
| CSV | Input datasets |
| JSON | Execution and reconciliation reports |

## 4. Dataset

The pipeline uses reproducible synthetic datasets.

| Dataset | Records |
|---|---:|
| Customers | 10,000 |
| Orders | 100,000 |

### Customer Schema

- customer_id
- customer_name
- email
- city
- created_at

### Order Schema

- order_id
- customer_id
- order_date
- amount
- status

## 5. Data Validation

### Customer Validation
- Required field validation
- Duplicate customer ID detection
- Email format validation
- Created timestamp validation

### Order Validation
- Required field validation
- Duplicate order ID detection
- Positive amount validation
- Order date validation
- Order status validation
- Customer reference integrity

Invalid records are separated into reject datasets with source row information and rejection reasons.

## 6. Transformations

### Customer Transformation
- Standardized customer names
- Normalized email addresses
- Parsed customer timestamps
- Derived customer creation date

### Order Transformation
- Standardized order status
- Converted order amounts
- Parsed order dates
- Derived order year and month

### Customer Order Summary
- Total orders
- Completed orders
- Completed revenue
- Average completed order value

## 7. Published Outputs

Curated datasets are published in Parquet format:

- `customers_curated.parquet`
- `orders_curated.parquet`
- `customer_order_summary.parquet`

Reject datasets:

- `customer_rejects.csv`
- `order_rejects.csv`
- `all_rejects.csv`

Operational reports:

- Run execution JSON
- Reconciliation JSON

## 8. Reliability and Observability

The pipeline supports:

- Unique execution identifiers
- Execution duration measurement
- Run status tracking
- Validation statistics
- Reject tracking
- Reconciliation checks
- Atomic replacement of individual Parquet outputs
- Idempotent publishing
- Automated failure-recovery testing

## 9. Reconciliation

The pipeline reconciles input, valid, rejected, and published records.

It also compares input and valid order amounts.

Successful reconciliation confirms that processing counts and published datasets match the expected pipeline results.

## 10. Performance Benchmark

A benchmark was executed using:

- 10,000 customers
- 100,000 orders

Observed pipeline benchmark:

- Execution time: approximately 10.786 seconds
- Throughput: approximately 9,270 orders/second

A separate full pipeline execution completed in 9.837 seconds.

Performance measurements are environment-dependent.

## 11. Installation

Clone or download the project.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 12. Execute Pipeline

```bash
python -m src.main
```

## 13. Generate Synthetic Data

```bash
python scripts/generate_data.py
```

The generator supports reproducible synthetic data generation using a fixed random seed.

## 14. Run Tests

```bash
python -m pytest -v
```

Current automated test result:

**14 tests passed**

## 15. Benchmark

```bash
python benchmarks/benchmark.py
```

## 16. Project Structure

```text
yottaflex-data-pipeline/
├── src/
├── tests/
├── scripts/
├── benchmarks/
├── data/
│   ├── input/
│   ├── output/
│   └── rejects/
├── reports/
├── docs/
├── requirements.txt
└── README.md
```

## 17. Future Improvements

- Distributed processing using Apache Spark
- Incremental ingestion
- Configurable validation rules
- Data lineage tracking
- Pipeline orchestration
- Monitoring and alerting
- Cloud deployment
- Multi-dataset transactional publishing

## Conclusion

This project demonstrates a reproducible batch data engineering pipeline with data validation, transformations, curated publishing, reconciliation, observability, and automated reliability testing.