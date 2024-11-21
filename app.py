from pyspark.sql import SparkSession

# Создаём сессию Spark
spark = SparkSession.builder \
    .appName("PySpark ClickHouse Connection") \
    .config("spark.jars", "/home/hek/my_dir/clickhouse-jdbc-0.4.6.jar,/home/hek/my_dir/postgresql-42.2.23.jar") \
    .getOrCreate()

# Параметры подключения PostgreSQL
postgresql_url = "jdbc:postgresql://192.168.1.35:5444/testdb"
postgresql_properties = {
    "user": "postgres",
    "password": "password",
    "driver": "org.postgresql.Driver"
}

# Чтение данных из PostgreSQL
postgres_df = spark.read.jdbc(url=postgresql_url, table="employees1", properties=postgresql_properties)

print("Данные из PostgrSQL:")
postgres_df.show()

# Параметры подключения ClickHouse
clickhouse_url = "jdbc:clickhouse://192.168.1.35:8123/default"
clickhouse_properties = {
    "user": "default",
    "password": "",
    "driver": "com.clickhouse.jdbc.ClickHouseDriver"
}

# Чтение данных из ClickHouse
clickhouse_df = spark.read.jdbc(url=clickhouse_url, table="employees2", properties=clickhouse_properties)

print("Данные из ClickHouse:")
clickhouse_df.show()
spark.stop()