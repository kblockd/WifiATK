CREATE DATABASE Wifi DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE USER 'wifi'@'localhost' IDENTIFIED BY 'WifiAttack123.';
CREATE USER 'wifi'@'%' IDENTIFIED BY 'WifiAttack123.';

GRANT ALL ON Wifi.* TO 'wifi'@'localhost';
GRANT ALL ON Wifi.* TO 'wifi'@'%';