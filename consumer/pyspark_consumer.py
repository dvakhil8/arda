import configparser
import os
import sys

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import from_json, col, explode, array, from_unixtime, window, row_number, count, \
    to_timestamp, current_timestamp, avg, min, lit
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, LongType, MapType, \
    ArrayType, DecimalType

blocks_schema = StructType([
    StructField('timestamp', LongType(), True),
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
]
)

transaction_schema = StructType(
    [
        StructField('hash', StringType(), True),
        StructField('nounce', DoubleType(), True),
        StructField('transaction_index', DoubleType(), True),
        StructField('from_address', StringType(), True),
        StructField('to_address', StringType(), True),
        StructField('value', DecimalType(38, 0), True),
        StructField('gas', DoubleType(), True),
        StructField('gas_price', DoubleType(), True),
        StructField('input', StringType(), True),
        StructField('receipt_cumulative_gas_used', DoubleType(), True),
        StructField('receipt_gas_used', DoubleType(), True),
        StructField('receipt_contract_address', StringType(), True),
        StructField('receipt_root', StringType(), True),
        StructField('receipt_status', DoubleType(), True),
        StructField('block_timestamp', LongType(), True),
        StructField('block_number', DoubleType(), True),
        StructField('block_hash', StringType(), True),
        StructField('max_fee_per_gas', DoubleType(), True),
        StructField('max_priority_fee_per_gas', DoubleType(), True),
        StructField('transaction_type', DoubleType(), True),
        StructField('receipt_effective_gas_price', DoubleType(), True)
    ]

)


class PysparkStreaming:
    def __int__(self):
        self.spark = self.getSparkSession()

    def getSparkSession(self):
        spark = SparkSession \
            .builder \
            .appName("blocks_event_spark") \
            .config("spark.sql.debug.maxToStringFields", "100") \
            .getOrCreate()
        spark.sparkContext.setLogLevel("warn")
        return spark

    def getKafkaStream(self, bootstrap_servers):
        print(bootstrap_servers)
        return self.getSparkSession() \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", bootstrap_servers) \
            .option("spark.driver.memory", "2g") \
            .option("subscribe", "transactions") \
            .option("startingOffsets", "latest") \
            .option("spark.streaming.kafka.maxRatePerPartition", "50") \
            .load()

    def writeStream(self,df):
        query = df.writeStream.format("console").start()
        query.awaitTermination()

    def getTotalGasHour(self,df):
        df = df.selectExpr("CAST(value AS STRING)")
        df = df.withColumn("parsed_value", from_json(col('value'), transaction_schema)) \
            .withColumn("exploded", explode(array("parsed_value"))) \
            .select("exploded.*")
        df = df.withColumn('event_timestamp', current_timestamp())
        df = df.withColumn("block_timestamp_ts", to_timestamp(from_unixtime(df.block_timestamp)))
        df = df.withColumn("block_timestamp_hourly",
                           to_timestamp(from_unixtime(col('block_timestamp'), "yyyy-MM-dd HH")))
        df = df.withColumn("gas_value", col('gas') * col('gas_price'))
        df1 = df.withWatermark("block_timestamp_hourly", "60 minutes").groupby("block_timestamp_hourly").sum(
            'gas_value')
        return df1
    def startStreaming(self, bootstrap_servers):
        sourceDf = self.getKafkaStream(bootstrap_servers)
        writeStreamDf = self.getTotalGasHour(sourceDf)
        self.writeStream(writeStreamDf)


if __name__ == "__main__":
    if os.environ.get('CONFIG_FILE', -1) != -1:
        config = configparser.ConfigParser()
        config.read(os.environ.get('CONFIG_FILE'))
        kafka_config = config['Kafka']
        streaming = PysparkStreaming()
        streaming.startStreaming(kafka_config['bootstrap_servers'])

    else:
        raise FileNotFoundError('config file not found. please set CONFIG_FILE env variable')
