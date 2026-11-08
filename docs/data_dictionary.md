# Data Dictionary

## 1. Customers Dataset

| Column | Data Type | Key | Description |
|---|---|---|---|
| customer_id | String | Primary Key | Unique customer identifier |
| customer_name | String | — | Customer name |
| email | String | — | Customer email address |
| city | String | — | Customer city |
| created_at | Timestamp | — | Customer registration timestamp |

### Customer Rules
- `customer_id` must be present and unique.
- `customer_name` must not be empty.
- `email` must follow a valid email format.
- `city` must not be empty.
- `created_at` must be a valid timestamp.

## 2. Orders Dataset

| Column | Data Type | Key | Description |
|---|---|---|---|
| order_id | String | Primary Key | Unique order identifier |
| customer_id | String | Foreign Key | References customers |
| order_date | Date/Timestamp | — | Order creation date |
| amount | Decimal | — | Order transaction amount |
| status | String | — | Order lifecycle status |

### Order Rules
- `order_id` must be present and unique.
- `customer_id` must reference a valid customer.
- `amount` must be greater than zero.
- `order_date` must be valid.
- Status must be COMPLETED, PENDING, or CANCELLED.

## 3. Customer Order Summary

| Column | Data Type | Description |
|---|---|---|
| customer_id | String | Customer identifier |
| customer_name | String | Customer name |
| email | String | Customer email |
| city | String | Customer city |
| total_orders | Integer | Total orders |
| completed_orders | Integer | Completed orders |
| completed_revenue | Decimal | Revenue from completed orders |
| average_completed_order_value | Decimal | Average completed order value |

## 4. Derived Fields

### Orders
- `order_year`: Year extracted from order date.
- `order_month`: Month extracted from order date.

### Customers
- `customer_created_date`: Date extracted from created timestamp.

## 5. Reject Metadata

| Column | Description |
|---|---|
| source_file | Original input filename |
| source_row | Original CSV row number |
| run_id | Pipeline execution identifier |
| reject_reason | Validation failure explanation |
| reject_code | Validation failure category |

## 6. Assumptions

- Customer and order identifiers are strings.
- Each order belongs to one customer.
- Customer IDs are unique.
- Order IDs are unique.
- Only valid customer references are accepted.
- Order amounts must be positive.
- Revenue is calculated only for COMPLETED orders.
- Invalid records are rejected rather than silently corrected.
- Processing is batch-oriented.
- Synthetic datasets are used for reproducibility.