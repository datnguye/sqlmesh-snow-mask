MODEL (
    name jf.raw_customers,
    kind SEED (
        path '../../seeds/raw_customers.csv'
    ),
    columns (
        id INTEGER,
        first_name STRING,
        last_name STRING
    ),
    grain [id]
);
