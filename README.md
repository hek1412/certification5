# Certification 5 1T (DevOps)
## Задание 5. Создание Docker-контейнера с PostgreSQL и ClickHouse
### PySpark ClickHouse Connection
В рамках этого задания необходимо развернуть базы данных PostgreSQL и ClickHouse в Docker с использованием Docker Compose, создавать таблицы и данные в этих базах данных, а затем использовать PySpark для чтения данных из обеих баз данных и работы с ними в рамках одного DataFrame.

Для начала преготовим SQL запросы для создания таблиц и внесения в них данных:
1) Для PostgreSQL
```
CREATE TABLE IF NOT EXISTS employees1 (id SERIAL PRIMARY KEY, name VARCHAR(255), age SMALLINT, salary DECIMAL(10, 2));
INSERT INTO employees1 (name, age, salary) VALUES ('John', 25, 50000), ('Jane', 30, 60000), ('Mike', 35, 70000), ('Emily', 40, 80000), ('William', 28, 55000), ('Linda', 32, 62000), ('David', 38, 72000), ('Susan', 45, 82000), ('Maria', 29, 56000), ('James', 33, 63000);

```
2) Для ClickHouse
```
CREATE TABLE IF NOT EXISTS  employees2 (id Int32, name String, age Float32, salary Float64) ENGINE = MergeTree()
ORDER BY id;
INSERT INTO employees2 (id, name, age, salary) VALUES (1, 'John', 25, 50000), (2, 'Jane', 30, 60000), (3, 'Mike', 35, 70000), (4, 'Emily', 40, 80000), (5, 'William', 28, 55000), (6, 'Linda', 32, 62000), (7, 'David', 38, 72000), (8, 'Sophia', 29, 58000), (9, 'Maria', 29, 56000), (10, 'James', 33, 63000);
```
Сохраняем данные файлы, название не имеет значения, но их необходимо поместить в отдельные папки в директории нашего преоекта.

Далее создаем docker-compose для развертывания наших баз, не забываем указать в volumes созданные папки с запросами для их инициализации при создании контейнеров:

```
services:
  clickhouse:
    image: clickhouse/clickhouse-server:23.10.4.25-alpine
    container_name: clickhouse_container
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - ./init_clickhouse:/docker-entrypoint-initdb.d
    networks:
      - postgres-click

  postgres:
    image: postgres:12.21
    restart: always
    container_name: postgres_container
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: testdb
    ports:
      - "5444:5432"
    volumes:
      - local_postgres_data:/var/lib/postgresql/data
      - ./init_postgres:/docker-entrypoint-initdb.d
networks:
  postgres-click:
    driver: bridge
volumes:
  local_postgres_data:
```

Вводим команду в терминале (перед этим необходимо убедиться, что все файлы в созданной директории) 
```
docker-compose up -d
```

Убедимся, что все работает, контейнеры в статусе UP
```
docker ps
```
![Результат.](/1.png)

Посмотрим логи в каждом контейнере: 
![Результат.](/2.png)
![Результат.](/3.png)

Отлично ошибок нет, отлично!)))

Так же подключимся с локального DBeaver к базам и сделаем Select (используем необходимые данные по портам и переменным средам из docker-compose)
![Результат.](/4.png)

Отлично! Теперь идем в виртуальную машину с Ubuntu (костыли с установкой PySpark на Win 10 мне ясны, но у меня уже было все утановлено на VM)

Создаем app.py для подключения и чтения данных на установленных в Docker базах данных (в данном случае помещаем jdbc драйвера в директорию с app.py):

```
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
```

Запускаем созданный скрипт и наслаждаемся результатом))))
![Результат.](/5.png)


