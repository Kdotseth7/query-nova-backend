-- Insert synthetic data into usr table
INSERT INTO usr (name, email, status)
SELECT
    'User ' || i,
    'user' || i || '@example.com',
    CASE WHEN i % 2 = 0 THEN 'active' ELSE 'inactive' END
FROM generate_series(1, 50) AS i;

-- Insert synthetic data into prod table
INSERT INTO prod (name, description, price, stock)
SELECT
    'Product ' || i,
    'Description for product ' || i,
    ROUND((random() * 100)::numeric, 2),
    (random() * 100)::INT
FROM generate_series(1, 50) AS i;

-- Insert synthetic data into ord table
INSERT INTO ord (user_id, product_id, quantity)
SELECT
    (random() * 49 + 1)::INT,
    (random() * 49 + 1)::INT,
    (random() * 10)::INT
FROM generate_series(1, 100) AS i;

-- Insert synthetic data into wh table
INSERT INTO wh (name, location, capacity, manager)
SELECT
    'Warehouse ' || i,
    'Location ' || i,
    (random() * 1000)::INT,
    'Manager ' || i
FROM generate_series(1, 10) AS i;

-- Insert synthetic data into inv table
INSERT INTO inv (product_id, warehouse_id, quantity)
SELECT
    (random() * 49 + 1)::INT,
    (random() * 9 + 1)::INT,
    (random() * 100)::INT
FROM generate_series(1, 50) AS i;

-- Insert synthetic data into sup table
INSERT INTO sup (name, contact_name, phone, email)
SELECT
    'Supplier ' || i,
    'Contact ' || i,
    '123-456-789' || i,
    'supplier' || i || '@example.com'
FROM generate_series(1, 10) AS i;

-- Insert synthetic data into emp table
INSERT INTO emp (name, position, salary)
SELECT
    'Employee ' || i,
    CASE WHEN i % 2 = 0 THEN 'Developer' ELSE 'Manager' END,
    ROUND((random() * 100000)::numeric, 2)
FROM generate_series(1, 20) AS i;

-- Insert synthetic data into dept table
INSERT INTO dept (name, manager_id, location, budget)
SELECT
    'Department ' || i,
    (random() * 19 + 1)::INT,
    'Location ' || i,
    ROUND((random() * 1000000)::numeric, 2)
FROM generate_series(1, 5) AS i;

-- Insert synthetic data into proj table
INSERT INTO proj (name, department_id, end_date)
SELECT
    'Project ' || i,
    (random() * 4 + 1)::INT,
    CURRENT_DATE + (random() * 100)::INT
FROM generate_series(1, 10) AS i;

-- Insert synthetic data into task table
INSERT INTO task (project_id, name, assigned_to, due_date)
SELECT
    (random() * 9 + 1)::INT,
    'Task ' || i,
    (random() * 19 + 1)::INT,
    CURRENT_DATE + (random() * 50)::INT
FROM generate_series(1, 20) AS i;

COMMIT;