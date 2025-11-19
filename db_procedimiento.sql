-- Active: 1755654599943@@127.0.0.1@3306@tienda_db
/* Crear la base de datos*/
CREATE DATABASE tienda_db;

USE tienda_db;


/* Crear procedimiento*/
DELIMITER //

CREATE PROCEDURE actualizar_precio_producto(
    IN p_nombre VARCHAR(100),
    IN p_porcentaje DECIMAL(5,2)
)
BEGIN
    UPDATE tienda_app_producto
    SET precio = ROUND(precio * (1 + p_porcentaje / 100), 2)
    WHERE nombre = p_nombre;
END //

DELIMITER ;