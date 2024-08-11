-- Create tables without descriptions
CREATE TABLE usr (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20)
);

CREATE TABLE ord (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES usr(user_id),
    product_id INT,
    quantity INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prod (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    description TEXT,
    price DECIMAL(10, 2),
    stock INT
);

CREATE TABLE inv (
    inventory_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES prod(product_id),
    warehouse_id INT,
    quantity INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE wh (
    warehouse_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    location VARCHAR(100),
    capacity INT,
    manager VARCHAR(50)
);

CREATE TABLE sup (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    contact_name VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(50)
);

CREATE TABLE emp (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    position VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dept (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    manager_id INT REFERENCES emp(employee_id),
    location VARCHAR(100),
    budget DECIMAL(10, 2)
);

CREATE TABLE proj (
    project_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    department_id INT REFERENCES dept(department_id),
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP
);

CREATE TABLE task (
    task_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES proj(project_id),
    name VARCHAR(50),
    assigned_to INT REFERENCES emp(employee_id),
    due_date TIMESTAMP
);

-- Add comments to tables
COMMENT ON TABLE usr IS 'User information table';
COMMENT ON TABLE ord IS 'Order information table';
COMMENT ON TABLE prod IS 'Product information table';
COMMENT ON TABLE inv IS 'Inventory information table';
COMMENT ON TABLE wh IS 'Warehouse information table';
COMMENT ON TABLE sup IS 'Supplier information table';
COMMENT ON TABLE emp IS 'Employee information table';
COMMENT ON TABLE dept IS 'Department information table';
COMMENT ON TABLE proj IS 'Project information table';
COMMENT ON TABLE task IS 'Task information table';

-- Add comments to columns
COMMENT ON COLUMN usr.user_id IS 'Primary key for users';
COMMENT ON COLUMN usr.name IS 'Name of the user';
COMMENT ON COLUMN usr.email IS 'Email of the user';
COMMENT ON COLUMN usr.created_at IS 'Account creation timestamp';
COMMENT ON COLUMN usr.status IS 'Current status of the user';

COMMENT ON COLUMN ord.order_id IS 'Primary key for orders';
COMMENT ON COLUMN ord.user_id IS 'User ID who placed the order';
COMMENT ON COLUMN ord.product_id IS 'Product ID ordered';
COMMENT ON COLUMN ord.quantity IS 'Quantity of the product ordered';
COMMENT ON COLUMN ord.order_date IS 'Date when the order was placed';

COMMENT ON COLUMN prod.product_id IS 'Primary key for products';
COMMENT ON COLUMN prod.name IS 'Name of the product';
COMMENT ON COLUMN prod.description IS 'Description of the product';
COMMENT ON COLUMN prod.price IS 'Price of the product';
COMMENT ON COLUMN prod.stock IS 'Stock available for the product';

COMMENT ON COLUMN inv.inventory_id IS 'Primary key for inventory records';
COMMENT ON COLUMN inv.product_id IS 'Product ID in inventory';
COMMENT ON COLUMN inv.warehouse_id IS 'Warehouse ID where the product is stored';
COMMENT ON COLUMN inv.quantity IS 'Quantity of the product in inventory';
COMMENT ON COLUMN inv.last_updated IS 'Last updated timestamp of the inventory record';

COMMENT ON COLUMN wh.warehouse_id IS 'Primary key for warehouses';
COMMENT ON COLUMN wh.name IS 'Name of the warehouse';
COMMENT ON COLUMN wh.location IS 'Location of the warehouse';
COMMENT ON COLUMN wh.capacity IS 'Capacity of the warehouse';
COMMENT ON COLUMN wh.manager IS 'Manager of the warehouse';

COMMENT ON COLUMN sup.supplier_id IS 'Primary key for suppliers';
COMMENT ON COLUMN sup.name IS 'Name of the supplier';
COMMENT ON COLUMN sup.contact_name IS 'Contact person name at the supplier';
COMMENT ON COLUMN sup.phone IS 'Phone number of the supplier';
COMMENT ON COLUMN sup.email IS 'Email of the supplier';

COMMENT ON COLUMN emp.employee_id IS 'Primary key for employees';
COMMENT ON COLUMN emp.name IS 'Name of the employee';
COMMENT ON COLUMN emp.position IS 'Position of the employee';
COMMENT ON COLUMN emp.salary IS 'Salary of the employee';
COMMENT ON COLUMN emp.hire_date IS 'Hire date of the employee';

COMMENT ON COLUMN dept.department_id IS 'Primary key for departments';
COMMENT ON COLUMN dept.name IS 'Name of the department';
COMMENT ON COLUMN dept.manager_id IS 'Manager ID of the department';
COMMENT ON COLUMN dept.location IS 'Location of the department';
COMMENT ON COLUMN dept.budget IS 'Budget of the department';

COMMENT ON COLUMN proj.project_id IS 'Primary key for projects';
COMMENT ON COLUMN proj.name IS 'Name of the project';
COMMENT ON COLUMN proj.department_id IS 'Department ID responsible for the project';
COMMENT ON COLUMN proj.start_date IS 'Start date of the project';
COMMENT ON COLUMN proj.end_date IS 'End date of the project';

COMMENT ON COLUMN task.task_id IS 'Primary key for tasks';
COMMENT ON COLUMN task.project_id IS 'Project ID associated with the task';
COMMENT ON COLUMN task.name IS 'Name of the task';
COMMENT ON COLUMN task.assigned_to IS 'Employee ID assigned to the task';
COMMENT ON COLUMN task.due_date IS 'Due date for the task';

COMMIT ;