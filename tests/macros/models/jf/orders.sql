MODEL (
  name jf.orders,
  kind FULL,
  cron '@daily',
  grain [order_id]
);

@DEF(payment_methods, ['credit_card', 'coupon', 'bank_transfer', 'gift_card']);

WITH orders AS (
  SELECT
    *
  FROM jf.stg_orders
), payments AS (
  SELECT
    *
  FROM jf.stg_payments
), order_payments AS (
  SELECT
    order_id,
    @EACH(
      @payment_methods,
      x -> SUM(CASE WHEN payment_method = x THEN amount ELSE 0 END) AS amount_@x
    ),
    SUM(amount) AS total_amount
  FROM payments
  GROUP BY
    order_id
), final AS (
  SELECT
    orders.order_id,
    orders.customer_id,
    orders.order_date,
    orders.status,
    @EACH(@payment_methods, x -> order_payments.amount_@x),
    order_payments.total_amount AS amount
  FROM orders
  LEFT JOIN order_payments
    ON orders.order_id = order_payments.order_id
)
SELECT
  *
FROM final
