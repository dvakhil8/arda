import configparser
import os
from pyspark.sql import SparkSession
import sys


class SparkBatch:
    def getSparkSession(self):
        spark = SparkSession.builder.master('local').appName("appName").config("spark.driver.extraClassPath",
                                                                               "./clickhouse-native-jdbc-shaded-2.5.4"
                                                                               ".jar").getOrCreate()
        spark.sparkContext.setLogLevel("warn")
        return spark

    def readQueryfromFile(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', '')
        return data

    def process(self, clickhouse_config, file_path):
        pgDF = self.getSparkSession().read.format('jdbc').option('driver', clickhouse_config['driver']) \
            .option('url', clickhouse_config['url']).option('user', clickhouse_config['user']). \
            option('password', clickhouse_config['password']) \
            .option('query', self.readQueryfromFile(file_path)) \
            .load()

        pgDF.show()


if __name__ == "__main__":
    file_path = sys.argv[1]
    if os.environ.get('CONFIG_FILE', -1) != -1:
        config = configparser.ConfigParser()
        config.read(os.environ.get('CONFIG_FILE'))
        clickhouse_config = config['Clickhouse']
        streaming = SparkBatch()
        streaming.process(clickhouse_config, file_path)

    else:
        raise FileNotFoundError('config file not found. please set CONFIG_FILE env variable')
