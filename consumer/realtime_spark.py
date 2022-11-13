from pyspark.sql import SparkSession
import sys
print("===================================")
print(sys.argv)
print("===================================")
sql_script_path = sys.argv[1]
with open(sql_script_path, 'r') as file:
    data = file.read().replace('\n', '')
appName = "Connect To clickhouse - via JDBC"
spark = SparkSession.builder.master('local').appName(appName).config("spark.driver.extraClassPath",
                                                                     "./clickhouse-native-jdbc-shaded-2.5.4.jar").getOrCreate()

url = "jdbc:clickhouse://127.0.0.1:9000"
user = "default"  # replace by whatever you use
password = ""  # same here
dbtable = 'arda_test.blocks'
driver = "com.github.housepower.jdbc.ClickHouseDriver"
pgDF = spark.read.format('jdbc').option('driver', driver)\
    .option('url', url).option('user', user).\
    option('password',password)\
    .option('query',data) \
    .load()

pgDF.show()

