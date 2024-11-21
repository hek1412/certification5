-- SQL commands to create table and insert data for PostgreSQL
CREATE TABLE IF NOT EXISTS employees1 (id SERIAL PRIMARY KEY, name VARCHAR(255), age SMALLINT, salary DECIMAL(10, 2));
INSERT INTO employees1 (name, age, salary) VALUES ('John', 25, 50000), ('Jane', 30, 60000), ('Mike', 35, 70000), ('Emily', 40, 80000), ('William', 28, 55000), ('Linda', 32, 62000), ('David', 38, 72000), ('Susan', 45, 82000), ('Maria', 29, 56000), ('James', 33, 63000);

