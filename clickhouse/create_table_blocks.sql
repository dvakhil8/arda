
CREATE TABLE arda_test.blocks
(
    timestamp DateTime,
   number BIGINT,
   hash String  ,
    parent_hash String,
    nonce String,
    sha3_uncles String,
    logs_bloom String,
     transactions_root String,
state_root String,
receipts_root String,
miner String,
difficulty Numeric(38,0),
   total_difficulty Numeric(38,0),
   size BIGINT,
   extra_data String,
   gas_limit BIGINT,
   gas_used BIGINT,
   transaction_count BIGINT,
   base_fee_per_gas BIGINT
) ENGINE = MergeTree
PARTITION BY toYYYYMMDD(timestamp)
ORDER BY (timestamp);






CREATE TABLE arda_test.blocks_queue
(
    timestamp DateTime,
   number BIGINT,
   hash String  ,
    parent_hash String,
    nonce String,
    sha3_uncles String,
    logs_bloom String,
     transactions_root String,
state_root String,
receipts_root String,
miner String,
difficulty Numeric(38,0),
   total_difficulty Numeric(38,0),
   size BIGINT,
   extra_data String,
   gas_limit BIGINT,
   gas_used BIGINT,
   transaction_count BIGINT,
   base_fee_per_gas BIGINT
) ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'localhost:9092',
    kafka_topic_list = 'blocks',
    kafka_group_name = 'block_event_clickhouse',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 4;



CREATE MATERIALIZED VIEW arda_test.blocks_queue_mv TO arda_test.blocks AS
SELECT *
FROM arda_test.blocks_queue;



