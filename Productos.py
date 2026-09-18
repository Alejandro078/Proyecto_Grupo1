productos = []


# REGISTRAR PRODUCTO
def registrar_productos():
    print("\n--- REGISTRAR PRODUCTO ---")

    nombre = input("Nombre: ")
    descripcion = input("Descripción: ")
    categoria = input("Categoría: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))

    producto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "categoria": categoria,
        "precio": precio,
        "stock": stock
    }

    productos.append(producto)

    print("Producto registrado correctamente.")


# MOSTRAR PRODUCTOS
def mostrar_productos():
    print("\n--- PRODUCTOS ---")

    if len(productos) == 0:
        print("No hay productos registrados.")
        return

    for i, producto in enumerate(productos):
        print(f"\nProducto {i + 1}")
        print(f"Nombre: {producto['nombre']}")
        print(f"Descripción: {producto['descripcion']}")
        print(f"Categoría: {producto['categoria']}")
        print(f"Precio: {producto['precio']}")
        print(f"Stock: {producto['stock']}")


# EDITAR PRODUCTO
def editar_producto():
    mostrar_productos()

    if len(productos) == 0:
        return

    numero = int(input("\nDigite el número del producto que desea editar: "))

    if numero < 1 or numero > len(productos):
        print("Producto no válido.")
        return

    producto = productos[numero - 1]

    print("\n--- EDITAR PRODUCTO ---")

    producto["nombre"] = input("Nuevo nombre: ")
    producto["descripcion"] = input("Nueva descripción: ")
    producto["categoria"] = input("Nueva categoría: ")
    producto["precio"] = float(input("Nuevo precio: "))
    producto["stock"] = int(input("Nuevo stock: "))

    print("Producto actualizado correctamente.")


# ELIMINAR PRODUCTO
def eliminar_producto():
    mostrar_productos()

    if len(productos) == 0:
        return

    numero = int(input("\nDigite el número del producto que desea eliminar: "))

    if numero < 1 or numero > len(productos):
        print("Producto no válido.")
        return

    productos.pop(numero - 1)

    print("Producto eliminado correctamente.")




