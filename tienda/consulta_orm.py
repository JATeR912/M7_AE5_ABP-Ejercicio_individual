from tienda_app.models import Producto
from django.db.models import DecimalField, F, ExpressionWrapper
from django.db import connection

print("\n=== INICIO DE CONSULTAS ORM ===\n")

# -------------------------------------------------------
# 1. Crear 30 productos
# -------------------------------------------------------
productos = [
    Producto(nombre="Camiseta básica blanca", precio=9.99, disponible=True),
    Producto(nombre="Pantalón de mezclilla", precio=29.99, disponible=True),
    Producto(nombre="Chaqueta de cuero", precio=89.50, disponible=True),
    Producto(nombre="Zapatillas deportivas", precio=59.99, disponible=True),
    Producto(nombre="Sudadera con capucha", precio=34.99, disponible=True),
    Producto(nombre="Camisa formal azul", precio=24.50, disponible=False),
    Producto(nombre="Falda negra", precio=22.99, disponible=True),
    Producto(nombre="Sombrero de verano", precio=14.75, disponible=True),
    Producto(nombre="Bufanda de lana", precio=12.50, disponible=False),
    Producto(nombre="Guantes de invierno", precio=10.99, disponible=False),
    Producto(nombre="Reloj de pulsera", precio=79.99, disponible=False),
    Producto(nombre="Bolso de mano", precio=45.00, disponible=False),
    Producto(nombre="Cinturón de cuero", precio=19.99, disponible=True),
    Producto(nombre="Sandalias de playa", precio=15.50, disponible=False),
    Producto(nombre="Gorra deportiva", precio=11.99, disponible=True),
    Producto(nombre="Vestido de noche", precio=65.00, disponible=False),
    Producto(nombre="Pijama de algodón", precio=25.99, disponible=True),
    Producto(nombre="Calcetines (pack x3)", precio=8.49, disponible=True),
    Producto(nombre="Abrigo largo", precio=99.99, disponible=True),
    Producto(nombre="Traje formal", precio=120.00, disponible=True),
    Producto(nombre="Zapatos de vestir", precio=75.00, disponible=True),
    Producto(nombre="Chaleco elegante", precio=40.00, disponible=True),
    Producto(nombre="Bañador para hombre", precio=18.99, disponible=False),
    Producto(nombre="Bañador para mujer", precio=21.99, disponible=False),
    Producto(nombre="Lentes de sol", precio=29.50, disponible=True),
    Producto(nombre="Camiseta estampada", precio=13.99, disponible=False),
    Producto(nombre="Pantalones cortos", precio=19.49, disponible=True),
    Producto(nombre="Zapatos casuales", precio=54.99, disponible=True),
    Producto(nombre="Bolso tipo mochila", precio=39.99, disponible=False),
    Producto(nombre="Corbata de seda", precio=16.99, disponible=False),
]

Producto.objects.all().delete()
Producto.objects.bulk_create(productos)
print("→ 30 productos creados exitosamente.\n")

# -------------------------------------------------------
# 1. Recuperar registros
# -------------------------------------------------------
print("=== Todos los productos ===")
for p in Producto.objects.all():
    print(p.id, p.nombre, p.precio, p.disponible)

print("\n")

# -------------------------------------------------------
# 2. Filtros
# -------------------------------------------------------
print("=== Productos con precio > 50 ===")
for p in Producto.objects.filter(precio__gt=50):
    print(p.id, p.nombre, p.precio)

print("\n")

print("=== Productos cuyo nombre empieza con 'A' ===")
for p in Producto.objects.filter(nombre__startswith="A"):
    print(p.id, p.nombre, p.precio)

print("\n")

print("=== Productos disponibles ===")
for p in Producto.objects.filter(disponible=True):
    print(p.id, p.nombre, p.precio)

print("\n")

# -------------------------------------------------------
# 3. raw() simple con SQL
# -------------------------------------------------------
print("=== raw(): Productos precio < 100 ===")
for p in Producto.objects.raw("SELECT * FROM tienda_app_producto WHERE precio < %s", [100]):
    print(p.id, p.nombre, p.precio)

print("\n")

# -------------------------------------------------------
# 4. raw() mapeado al modelo
# -------------------------------------------------------
print("=== raw(): Mapeo con disponible = True ===")
for p in Producto.objects.raw("SELECT * FROM tienda_app_producto WHERE disponible = %s", [True]):
    print(p.id, p.nombre, p.precio, p.disponible)

print("\n")

# -------------------------------------------------------
# 5. Índices
# -------------------------------------------------------
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT COUNT(1) 
        FROM INFORMATION_SCHEMA.STATISTICS 
        WHERE table_schema=DATABASE() 
        AND table_name='tienda_app_producto' 
        AND index_name='idx_nombre';
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute("CREATE INDEX idx_nombre ON tienda_app_producto(nombre)")

print("=== Búsqueda usando índice ===")
list(Producto.objects.filter(nombre__startswith='C'))
print("→ Búsqueda realizada.\n")

# -------------------------------------------------------
# 6. Excluir campos (defer)
# -------------------------------------------------------
print("=== Productos sin cargar 'disponible' ===")
for p in Producto.objects.defer("disponible"):
    print(p.id, p.nombre, p.precio)

print("\n")

# -------------------------------------------------------
# 7. annotate() cálculos
# -------------------------------------------------------
print("=== Precio con impuesto (16%) ===")
for p in Producto.objects.annotate(
    precio_con_impuesto=ExpressionWrapper(F("precio") * 1.16, output_field=DecimalField())
):
    print(p.id, p.nombre, p.precio, round(p.precio_con_impuesto, 2))

print("\n")

# -------------------------------------------------------
# 8. raw() con parámetros
# -------------------------------------------------------
print("=== raw() usando parámetros ===")
limite = 50
for p in Producto.objects.raw("SELECT * FROM tienda_app_producto WHERE precio < %s", [limite]):
    print(p.id, p.nombre, p.precio)

print("\n")

# -------------------------------------------------------
# 9. SQL directo
# -------------------------------------------------------
print("=== SQL directo: INSERT, UPDATE, DELETE ===")
with connection.cursor() as cursor:
    cursor.execute(
        "INSERT INTO tienda_app_producto (nombre, precio, disponible) VALUES (%s, %s, %s)",
        ["Camiseta de algodón", 19.99, True]
    )
    cursor.execute(
        "UPDATE tienda_app_producto SET precio=%s WHERE nombre=%s",
        [29.99, "Camiseta de algodón"]
    )
    cursor.execute(
        "DELETE FROM tienda_app_producto WHERE nombre=%s",
        ["Camiseta de algodón"]
    )

print("→ SQL directo ejecutado.\n")

# -------------------------------------------------------
# 10. Conexiones y cursor manual
# -------------------------------------------------------
print("=== Datos usando cursor manual ===")
with connection.cursor() as cursor:
    cursor.execute("SELECT nombre, precio FROM tienda_app_producto LIMIT 5")
    
    for nombre, precio in cursor.fetchall():
        print(f"Producto: {nombre}, Precio: {precio}")

print("\n")

# -------------------------------------------------------
# 11. Procedimiento almacenado
# -------------------------------------------------------
print("=== Procedimiento almacenado: actualizar_precio_producto ===")
nombre_producto = "Chaqueta de cuero"
aumento = 16  # %

with connection.cursor() as cursor:
    cursor.callproc("actualizar_precio_producto", [nombre_producto, aumento])
    connection.commit()

producto = Producto.objects.get(nombre=nombre_producto)
print(f"Nuevo precio: {producto.nombre} = {producto.precio}\n")

print("\n=== FIN DE CONSULTAS ORM ===\n")
