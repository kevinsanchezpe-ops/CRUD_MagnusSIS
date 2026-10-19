"""MVP de inventario por consola para la entrega 2.

Los productos se guardan únicamente en memoria y se pierden al salir.
Este programa no usa Django ni una base de datos.
"""


def agregar_producto(inventario):
    """Solicita y agrega un producto a la lista en memoria."""
    print("\nAgregar producto")
    nombre = input("Nombre del producto: ").strip()
    cantidad = int(input("Cantidad en stock: "))
    precio = float(input("Precio: "))

    inventario.append({
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio,
    })
    print("Producto agregado correctamente.")


def visualizar_inventario(inventario):
    """Muestra todos los productos registrados."""
    print("\nInventario")
    if not inventario:
        print("El inventario está vacío.")
        return

    for numero, producto in enumerate(inventario, start=1):
        print(
            f"{numero}. {producto['nombre']} | "
            f"Stock: {producto['cantidad']} | "
            f"Precio: ${producto['precio']:.2f}"
        )


def buscar_producto(inventario):
    """Busca productos por coincidencia parcial en el nombre."""
    termino = input("Nombre del producto que buscas: ").strip().casefold()
    resultados = [
        producto for producto in inventario
        if termino in producto["nombre"].casefold()
    ]

    if not resultados:
        print("No se encontraron productos con ese nombre.")
        return

    print("\nResultados")
    for producto in resultados:
        print(
            f"{producto['nombre']} | Stock: {producto['cantidad']} | "
            f"Precio: ${producto['precio']:.2f}"
        )


def mostrar_menu():
    """Imprime las opciones disponibles."""
    print("\n=== Magnus SIS · Inventario por consola ===")
    print("1. Agregar producto")
    print("2. Visualizar inventario")
    print("3. Buscar producto")
    print("4. Salir")


def main():
    """Mantiene el menú activo hasta que el usuario elija salir."""
    inventario = []

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            agregar_producto(inventario)
        elif opcion == "2":
            visualizar_inventario(inventario)
        elif opcion == "3":
            buscar_producto(inventario)
        elif opcion == "4":
            print("Hasta luego.")
            break
        else:
            print("Opción no reconocida. Elige una opción del 1 al 4.")


if __name__ == "__main__":
    main()
