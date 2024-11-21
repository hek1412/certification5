-- SQL commands for ClickHouse
CREATE TABLE IF NOT EXISTS  employees2 (id Int32, name String, age Float32, salary Float64) ENGINE = MergeTree()
ORDER BY id;
INSERT INTO employees2 (id, name, age, salary) VALUES (1, 'John', 25, 50000), (2, 'Jane', 30, 60000), (3, 'Mike', 35, 70000), (4, 'Emily', 40, 80000), (5, 'William', 28, 55000), (6, 'Linda', 32, 62000), (7, 'David', 38, 72000), (8, 'Sophia', 29, 58000), (9, 'Maria', 29, 56000), (10, 'James', 33, 63000);