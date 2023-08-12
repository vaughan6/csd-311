/*
    Title: db_init_company.sql
    Author: James Vaughan
    Date: 15 July 2020
    Description: company database initialization script.
*/

-- drop test user if exists 
DROP USER IF EXISTS 'company_user'@'localhost';


-- create company_user and grant them all privileges to the company database 
CREATE USER 'company_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MySQL8IsGreat!';

-- grant all privileges to the company database to user company_user on localhost 
GRANT ALL PRIVILEGES ON company.* TO'company_user'@'localhost';


-- drop tables if they are present
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS department;


-- create the department table 
CREATE TABLE department (
    department_id     INT             NOT NULL        AUTO_INCREMENT,
    department_name   VARCHAR(75)     NOT NULL,
    department_size      VARCHAR(75)     NOT NULL,
    PRIMARY KEY(department_id)
); 

-- create the employee table and set the foreign key
CREATE TABLE employee (
    employee_id   INT             NOT NULL        AUTO_INCREMENT,
    employee_name  VARCHAR(75)     NOT NULL,
    department_id     INT,
    birth_month   INT     NOT NULL,
    PRIMARY KEY(employee_id),
    FOREIGN KEY(department_id)
        REFERENCES department(department_id)
);


-- insert department records
INSERT INTO department(department_name, department_size)
    VALUES('HR', 1);

INSERT INTO department(department_name, department_size)
    VALUES('Finance', 1);

INSERT INTO department(department_name, department_size)
    VALUES('IT', 1);

INSERT INTO department(department_name, department_size)
    VALUES('Sales', 0);


-- insert employee records 
INSERT INTO employee(employee_name, birth_month, department_id) 
    VALUES('John', 1, (SELECT department_id FROM department WHERE department_name = 'HR'));

INSERT INTO employee(employee_name, birth_month, department_id)
    VALUES('Alice', 4, (SELECT department_id FROM department WHERE department_name = 'Finance'));

INSERT INTO employee(employee_name, birth_month, department_id)
    VALUES('Bob', 5, (SELECT department_id FROM department WHERE department_name = 'IT'));

INSERT INTO employee(employee_name, birth_month, department_id) 
    VALUES('Jack', 8, 104);

INSERT INTO employee(employee_name, birth_month, department_id)
    VALUES('Jill', 11, NULL);
