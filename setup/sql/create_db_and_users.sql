CREATE DATABASE bookstore;

-- I know this shouldn't be here if we were to be pedantic
-- done it for the sake of simplicity and reusability

CREATE USER web_user IDENTIFIED BY 'parolaweb_user';
CREATE USER db_manager IDENTIFIED BY 'paroladb_manager';
GRANT ALL PRIVILEGES ON *.* TO 'db_manager'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'web_user'@'%';
