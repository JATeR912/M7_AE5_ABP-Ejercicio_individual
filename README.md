## Proyecto: Consultas ORM y SQL en Django

Este proyecto demuestra el uso del ORM de Django, consultas SQL nativas, uso de cursores, procedimientos almacenados y manejo avanzado de consultas.

### Modelo utilizado

El proyecto usa el siguiente modelo:
```bash
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    disponible = models.BooleanField()

    def __str__(self):
        return f"Producto:{self.nombre} - Precio:{self.precio} - Disponible:{self.disponible}"
```

### Flujo de trabajo recomendado
1. Clonar el repositorio
```bash
git clone https://github.com/JATeR912/M7_AE5_ABP-Ejercicio_individual
cd nombre_proyecto
```
2. Crear y activar el entorno virtual

Linux / macOS:
```bash
python3 -m venv myenv
source myenv/bin/activate
```
Windows:
```bash
python -m venv myenv
venv\Scripts\activate
```
3. Instalar dependencias
```bash
pip install -r requirements.txt
```
4. Instalación del conector MySQL
Opción A — Usar mysqlclient (recomendado)
```bash
pip install mysqlclient
```
Opción B — Si falla, usar PyMySQL
```bash
pip install pymysql
```
Si usas PyMySQL, agregar al inicio de settings.py:
```bash
import pymysql
pymysql.install_as_MySQLdb()
```
5. Configurar la base de datos en settings.py
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tienda_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

6. Crear la base de datos en MySQL

Antes de migrar, crear la base de datos que usará Django:

```bash
CREATE DATABASE tienda_db;
``` 
#### 6.5. Asegúrate de estar en la carpeta donde está **manage.py**

Antes de ejecutar migraciones, levantar el servidor o usar la shell de Django, debes estar en la carpeta donde se encuentra el archivo:
**manage.py**

Ejemplo:
```bash
cd tienda            # ingresar a la carpeta que contiene manage.py
ls                   # verificar que aparece manage.py
```

7. Crear y aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

8. Crear procedimientos almacenados (requerido)

Después de aplicar las migraciones y que la tabla tienda_app_producto exista, crear el procedimiento:
```bash
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
```

9. Ejecutar la shell de Django
```bash
python manage.py shell
```
10. Ejecutar consultas en la ORM

Asegúrate de importar los modelos y herramientas:
```bash
from tienda_app.models import Producto
from django.db.models import DecimalField, F, ExpressionWrapper
from django.db import connection
```
### Explicación de las consultas

A continuación se detalla qué hace cada una de las consultas ejecutadas dentro de la shell de Django.

#### 1. Inserción de 30 productos y recuperación de registros

Se crean 30 objetos Producto para poblar la tabla.
Luego, se recuperan todos los registros almacenados en la base de datos.

Objetivo:
Verificar que la conexión, el modelo y las operaciones básicas del ORM funcionan correctamente.

#### 2. Aplicación de filtros

Se realizan tres tipos de filtros:

- Productos cuyo precio es mayor a 50

- Productos cuyo nombre comienza con la letra A

- Productos que están disponibles

Objetivo:
Demostrar el uso de operadores y condiciones mediante el ORM.

#### 3. Consulta SQL usando raw()

Se ejecuta una consulta SQL para obtener todos los productos cuyo precio es inferior a 100.

Objetivo:
Usar SQL puro dentro del ORM para consultas específicas.

#### 4. Uso de raw() mapeado al modelo

Se ejecuta una consulta SQL que devuelve únicamente los productos disponibles,
pero esta vez Django convierte automáticamente los resultados en objetos Producto.

Objetivo:
Demostrar que SQL externo puede integrarse con el ORM y seguir devolviendo modelos completos.

#### 5. Creación de un índice en la tabla

Se crea un índice sobre el campo nombre para optimizar búsquedas.

Objetivo:
Mejorar la velocidad de consultas que filtran por el nombre del producto, utilizando herramientas de MySQL desde Django.

Los índices son estructuras en la base de datos que aceleran la búsqueda de registros, similar al índice de un libro.
En Django se crean con db_index=True en un campo del modelo.

Impacto: Las consultas filter() o get() sobre campos indexados son mucho más rápidas, ya que la base de datos no necesita escanear toda la tabla.

#### 6. Exclusión de campos mediante defer

Se recuperan productos omitiendo un campo específico (disponible).

Objetivo:
Optimizar consultas cuando no se necesitan todos los campos, ahorrando memoria y tiempo de consulta.

Django maneja la omisión de campos con defer() o only().
Cuando se omite un campo:

- No se carga de la base de datos inicialmente, ahorrando recursos.

- Si se accede al campo después, Django ejecuta una consulta adicional solo para ese campo (carga diferida).

#### 7. Uso de anotaciones con annotate()

Se calcula un nuevo campo llamado precio_con_impuesto, incrementando el precio original en un 16%.

Objetivo:
Realizar cálculos directamente en la base de datos sin modificar los modelos ni la tabla.

#### 8. Consulta SQL con parámetros en raw()

Se ejecuta una consulta SQL asegurando que los valores se pasen como parámetros seguros, evitando inyección SQL.

Objetivo:
Demostrar buenas prácticas en consultas SQL externas.

El uso de parámetros asegura que los valores se escapen automáticamente, evitando inyección SQL.

Diferencia: en lugar de concatenar strings en el SQL, se usan placeholders (%s) y se pasan los valores por separado.

Beneficios: Seguridad, legibilidad y facilidad para reutilizar la misma consulta con distintos valores.

#### 9. Ejecución de SQL directo (INSERT, UPDATE, DELETE)

Se ejecutan instrucciones SQL manuales para:

- Insertar un producto

- Modificar su precio

- Eliminarlo

Objetivo:
Demostrar cómo ejecutar manipulación directa de datos sin pasar por el ORM.

Es recomendable utilizar SQL directo con cursor.execute() cuando:

- Se necesitan operaciones complejas que no se pueden hacer fácilmente con el ORM.

- Se requiere máxima eficiencia o control sobre la consulta SQL.

- Se ejecutan comandos administrativos o de mantenimiento.

**Precaución: Con el uso de cursor.execute() se pierde la abstracción del ORM y debes manejar manualmente seguridad y transacciones.**

#### 10. Uso manual del cursor de MySQL

Se ejecuta una consulta SQL que devuelve únicamente nombre y precio de algunos productos, usando el cursor directamente.

Objetivo:
Mostrar el manejo de conexiones manuales y lectura directa de registros desde MySQL.

Ventajas de usar cursor: permite control total sobre la consulta, iterar resultados grandes eficientemente.
Desventajas: requiere manejar manualmente transacciones y seguridad, no hay abstracción de ORM.

#### 11. Invocación de un procedimiento almacenado

Se ejecuta un procedimiento almacenado que aumenta el precio de un producto según un porcentaje indicado.

Este procedimiento debe existir previamente en la base de datos.

📄 Procedimiento almacenado (archivo SQL externo)
```bash
CREATE DATABASE tienda_db;
USE tienda_db;

DELIMITER //

CREATE PROCEDURE actualizar_precio_producto(
    IN p_nombre VARCHAR(100),
    IN p_porcentaje DECIMAL(5,2)
)
BEGIN
    UPDATE tienda_app_producto
    SET precio = ROUND(precio * (1 + p_porcentaje/100), 2)
    WHERE nombre = p_nombre;
END //

DELIMITER ;
```

Objetivo:
Demostrar cómo Django puede interactuar con lógica avanzada y optimizada en MySQL.