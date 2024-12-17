# Creating the `Azure Database for MySQL flexible servers` resource on Azure

Contrary to other resources, we suggest this resource be made by someone who knows what they are doing, because making a mistake here can be costly. That someone most likely will not need this guide though, either because they know how to create a database on Azure, or because a database service already exists.

If the latter is the case, the `console.sql` file in this directory contains how our database and database tables (names, types), and SQL triggers were set up. Our database is very basic, and your company most likely requires more nuance.

Below you can see some part of the entire script:

```sql
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projectTitle VARCHAR(255) NOT NULL,
    dateStarted DATETIME NOT NULL,
    isActive BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(100) NOT NULL,
    isAvailable BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE project_assignments (
     id INT AUTO_INCREMENT PRIMARY KEY,
     projectId INT NOT NULL,
     employeeId INT NOT NULL,
     assignedDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (projectId) REFERENCES projects(id) ON DELETE CASCADE,
     FOREIGN KEY (employeeId) REFERENCES employees(id) ON DELETE CASCADE
);
```
