from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType,MapType , LongType

blocks_schema = MapType(
    {
        StructField('timestamp', DoubleType(), True),
        StructField('number', DoubleType(), True),
        StructField('hash', StringType(), True),
        StructField('parent_hash', StringType(), True),
        StructField('nonce', StringType(), True),
        StructField('sha3_uncles', StringType(), True),
        StructField('logs_bloom', StringType(), True),
        StructField('transactions_root', StringType(), True),
        StructField('state_root', StringType(), True),
        StructField('receipts_root', StringType(), True),
        StructField('miner', StringType(), True),
        StructField('difficulty', DoubleType(), True),
        StructField('total_difficulty', DoubleType(), True),
        StructField('size', DoubleType(), True),
        StructField('extra_data', StringType(), True),
        StructField('gas_limit', DoubleType(), True),
        StructField('gas_used', DoubleType(), True),
        StructField('transaction_count', DoubleType(), True),
        StructField('base_fee_per_gas', DoubleType(), True)
    }
)

transaction_schema = StructType(
    [
        StructField('hash', StringType(), True),
        StructField('nounce', DoubleType(), True),
        StructField('transaction_index', DoubleType(), True),
        StructField('from_address', StringType(), True),
        StructField('to_address', StringType(), True),
        StructField('value', DoubleType(), True),
        StructField('gas', DoubleType(), True),
        StructField('gas_price', DoubleType(), True),
        StructField('input', StringType(), True),
        StructField('receipt_cumulative_gas_used', DoubleType(), True),
        StructField('receipt_gas_used', DoubleType(), True),
        StructField('receipt_contract_address', StringType(), True),
        StructField('receipt_root', StringType(), True),
        StructField('receipt_status', DoubleType(), True),
        StructField('block_timestamp', TimestampType(), True),
        StructField('block_number', DoubleType(), True),
        StructField('block_hash', StringType(), True),
        StructField('max_fee_per_gas', DoubleType(), True),
        StructField('max_priority_fee_per_gas', DoubleType(), True),
        StructField('transaction_type', DoubleType(), True),
        StructField('receipt_effective_gas_price', DoubleType(), True)

    ]

)
