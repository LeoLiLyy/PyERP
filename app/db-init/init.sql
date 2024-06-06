CREATE DATABASE pyerp;

USE pyerp;

CREATE TABLE employee (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(20) NULL,
    Dept VARCHAR(30) NULL,
    Email VARCHAR(30) UNIQUE NOT NULL,
    Password VARCHAR(90) NOT NULL,
    session_token VARCHAR(100) NULL
);

INSERT INTO employee (Name, Dept, Email, Password) VALUES ('Admin', 'Admin', 'admin@example.com', SHA2('adminpassword', 256));

CREATE TABLE inventory (
    ItemID INT AUTO_INCREMENT PRIMARY KEY,
    I_Name VARCHAR(20) NULL,
    I_Disc VARCHAR(500) NULL,
    InDate VARCHAR(10) NULL,
    OutDate VARCHAR(10) NULL,
    Warehouse_Num INT NULL,
    Quantity INT NULL
);

CREATE TABLE project (
    ProjectID INT AUTO_INCREMENT PRIMARY KEY,
    P_Name VARCHAR(20) NULL,
    P_Disc VARCHAR(500) NULL,
    Deadline VARCHAR(10) NULL,
    Products VARCHAR(500) NULL,
    Customer VARCHAR(100) NULL
);
