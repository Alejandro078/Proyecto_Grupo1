Cliente = []

#registrar un cliente
def RegistrarCliente():
    print("Registrar Cliente")
    nombre = input("Ingrese el nombre del cliente: ")
    apellido = input("Ingrese el apellido del cliente: ")
    correo = input("Ingrese el correo electrónico del cliente: ")
    telefono = input("Ingrese el número de teléfono del cliente: ")

    cliente = {
        "nombre": nombre,
        "apellido": apellido,
        "correo": correo,
        "telefono": telefono
    }

    Cliente.append(cliente)
    print("Cliente registrado exitosamente.")

#mostrar clientes
def ListaClientes():
    print("Lista de Clientes:")
    for cliente in Cliente:
         print(f"Nombre: {cliente['nombre']}, Apellido: {cliente['apellido']}, Correo: {cliente['correo']}, Teléfono: {cliente['telefono']}")


#editar cliente
def EditarCliente():
    print("Editar Cliente")
    correo = input("Ingrese el correo electrónico del cliente a editar: ")
    for cliente in Cliente:
        if cliente['correo'] == correo:
            nombre = input("Ingrese el nuevo nombre del cliente: ")
            apellido = input("Ingrese el nuevo apellido del cliente: ")
            telefono = input("Ingrese el nuevo número de teléfono del cliente: ")

            cliente['nombre'] = nombre
            cliente['apellido'] = apellido
            cliente['telefono'] = telefono

            print("Cliente editado exitosamente.")
            return
    print("Cliente no encontrado.")


#eliminar cliente
def EliminarCliente():
    print("Eliminar Cliente")
    correo = input("Ingrese el correo electrónico del cliente a eliminar: ")
    for cliente in Cliente:
        if cliente['correo'] == correo:
            Cliente.remove(cliente)
            print("Cliente eliminado exitosamente.")
            return
    print("Cliente no encontrado.")    

    
            