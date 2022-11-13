
CREATE TABLE arda_test.transactions
(
    hash String,
     nounce BIGINT,
    transaction_index BIGINT,
    from_address String,
    to_address String,
    value Numeric(38,0),
    gas BIGINT,
    gas_price BIGINT,
    input String,
    receipt_cumulative_gas_used BIGINT,
    receipt_gas_used BIGINT,
    receipt_contract_address String,
    receipt_root String,
    receipt_status BIGINT,
    block_timestamp DATETIME,
    block_number BIGINT,
    block_hash String,
    max_fee_per_gas BIGINT,
    max_priority_fee_per_gas BIGINT,
    transaction_type BIGINT,
    receipt_effective_gas_price BIGINT

) ENGINE = MergeTree
PARTITION BY toYYYYMMDD(block_timestamp)
ORDER BY (block_timestamp);






CREATE TABLE arda_test.transactions_queue
(
    hash String,
    nounce BIGINT,
    transaction_index BIGINT,
    from_address String,
    to_address String,
    value Numeric(38,0),
    gas BIGINT,
    gas_price BIGINT,
    input String,
    receipt_cumulative_gas_used BIGINT,
    receipt_gas_used BIGINT,
    receipt_contract_address String,
    receipt_root String,
    receipt_status BIGINT,
    block_timestamp DATETIME,
    block_number BIGINT,
    block_hash String,
    max_fee_per_gas BIGINT,
    max_priority_fee_per_gas BIGINT,
    transaction_type BIGINT,
    receipt_effective_gas_price BIGINT
) ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'localhost:9092',
    kafka_topic_list = 'blocks',
    kafka_group_name = 'block_event_clickhouse',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 4;



CREATE MATERIALIZED VIEW arda_test.transactions_queue_mv TO arda_test.transactions AS
SELECT *
FROM arda_test.transactions_queue;



