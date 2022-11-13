reference link to the problem statement -> https://gist.github.com/ramkumarvenkat/cb8550dbac0e201c3fb4df6e4708f44e

## **Project Setup**

```angular2html
    * Install and run zookeeper / kafka . ref -> https://kafka.apache.org/quickstart
    * Install and run clickhouse db . ref -> https://clickhouse.com/docs/en/quick-start/
    * After installing clickhouse db go to http://localhost:8123/play  and run clickhouse/create_table_blocks.sql & clickhouse/create_table_transactions.sql queries.
    * download , install spark and set $SPARK_HOME
```

```angular2html
    export CONFIG_FILE=/path/to/config_file.ini   -> update config_file.ini values with your own server endpoints
    git clone 
    cd arda
    pip install -r requirements.txt

    python3 producer/kafka_producer.py            -> will start producing blocks.csv and transactions.csv  to kafka broker. 

    ${SPARK_HOME}/bin/spark-submit                -> specifiy path to sql query and run it on spark as below command
          --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1
          --driver-class-path clickhouse-native-jdbc-shaded-2.6.5.jar 
          --jars clickhouse-native-jdbc-shaded-2.6.5.jar
            consumer/realtime_spark.py {path_to_sql_query}

    
    ${SPARK_HOME}/bin/spark-submit                 -> spark-structured-streaming of Total value of gas every hour.     
          --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1
            consumer/pyspark_consumer.py
```

## **Explaination**

* When installing clickhouse and running create table queries, we create a pipe between clickhouse and kafka. Any event pushed to  the topic will be consumed by clickhouse queue and inserted into blocks & transaction tables . 
* **producer/kafka_producer.py**  reads the csv files and pushed  the event to kafka.
* **consumer/realtime_spark.py** reads path to query as input and run's the query on spark-clickhouse connector. 
* **consumer/pyspark_consumer.py** starts a spark streaming consumer from kafka and dumps Total value of gas every hour into console / output file .
* **clickhouse/adhoc.sql** this file contains query which needs to be run on **http://localhost:8123/play** or can pass it through as path parameter to  **consumer/realtime_spark.py** file and fetch results.
* **clickhouse/realtime_analytics/*.sql** each file here refers to realtime analytics questions in the problem statement link. 




