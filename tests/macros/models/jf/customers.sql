MODEL (
  name jf.customers,
  kind FULL,
  cron '@daily',
  grain ARRAY[customer_id]
);


CREATE SCHEMA IF NOT EXISTS common; /* prepare mp */
CREATE TABLE IF NOT EXISTS common.log (
  id VARCHAR
); /* for faking mp */
@create_masking_policy(common.mp_first_name, None, TRUE); /* @create_masking_policy(common.mp_first_name); */
@create_masking_policy(common.mp_last_name, None, TRUE);/* @create_masking_policy(common.mp_last_name); */

WITH customers AS (
  SELECT
    *, @make_indicators('vehicle', ARRAY['truck', 'bus'])
  FROM jf.stg_customers
), orders AS (
  SELECT
    *
  FROM jf.stg_orders
), payments AS (
  SELECT
    *
  FROM jf.stg_payments
), customer_orders AS (
  SELECT
    customer_id,
    MIN(order_date) AS first_order,
    MAX(order_date) AS most_recent_order,
    COUNT(order_id) AS number_of_orders
  FROM orders
  GROUP BY
    customer_id
), customer_payments AS (
  SELECT
    orders.customer_id,
    SUM(amount) AS total_amount
  FROM payments
  LEFT JOIN orders
    ON payments.order_id = orders.order_id
  GROUP BY
    orders.customer_id
), final AS (
  SELECT
    customers.customer_id,
    customers.first_name,
    customers.last_name,
    concat(customers.first_name, customers.last_name) as full_name,
    customer_orders.first_order,
    customer_orders.most_recent_order,
    customer_orders.number_of_orders,
    customer_payments.total_amount AS customer_lifetime_value
  FROM customers
  LEFT JOIN customer_orders
    ON customers.customer_id = customer_orders.customer_id
  LEFT JOIN customer_payments
    ON customers.customer_id = customer_payments.customer_id
)
SELECT
  *
FROM final;

@apply_masking_policy(jf.customers, first_name, common.mp_first_name, ARRAY[], 'VIEW', TRUE); /* @apply_masking_policy(jf.customers, first_name, common.mp_first_name, ARRAY[]); */
@apply_masking_policy(jf.customers, last_name, common.mp_last_name, ARRAY['full_name'], 'VIEW', TRUE); /* @apply_masking_policy(jf.customers, last_name, common.mp_last_name, ARRAY['full_name']); */
