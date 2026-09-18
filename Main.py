import Productos
import Cliente

while True:
    print("\n==============================")
    print("       SISTEMA DE VENTAS")
    print("==============================")
    print("1. Gestión de productos")
    print("2. Gestión de clientes")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        while True:
            print("\n------------------------------")
            print("     GESTIÓN DE PRODUCTOS")
            print("------------------------------")
            print("1. Registrar producto")
            print("2. Mostrar productos")
            print("3. Editar producto")
            print("4. Eliminar producto")
            print("5. Volver al menú principal")

            opcion_producto = input("Seleccione una opción: ")

            if opcion_producto == "1":
               Productos.registrar_productos()

            elif opcion_producto == "2":
                Productos.mostrar_productos()

            elif opcion_producto == "3":
                Productos.editar_productos()

            elif opcion_producto == "4":
                Productos.eliminar_productos()

            elif opcion_producto == "5":
                break

            else:
                print("Opción no válida.")

    elif opcion == "2":
        while True:
            print("\n------------------------------")
            print("       GESTIÓN DE CLIENTES")
            print("------------------------------")
            print("1. Registrar cliente")
            print("2. Mostrar clientes")
            print("3. Editar cliente")
            print("4. Eliminar cliente")
            print("5. Volver al menú principal")

            opcion_cliente = input("Seleccione una opción: ")

            if opcion_cliente == "1":
                Cliente.registrar_clientes()

            elif opcion_cliente == "2":
                Cliente.mostrar_clientes()

            elif opcion_cliente == "3":
                Cliente.editar_clientes()

            elif opcion_cliente == "4":
                Cliente.eliminar_clientes()

            elif opcion_cliente == "5":
                break

            else:
                print("Opción no válida.")

    elif opcion == "3":
        print("Programa finalizado.")
        break

    else:
        print("Opción no válida.")