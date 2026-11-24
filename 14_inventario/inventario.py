import csv
import threading
import time

inventario = {}
mutex = threading.Lock()
with open("inventario.csv", "r", encoding="utf-8-sig") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        id_producto = int(fila["id_producto"])
        inventario [id_producto] = {
           "nombre": fila["nombre"],
           "categoria": fila["categoria"] ,
           "precio": float(fila["precio"]),
           "cantidad": float(fila["cantidad"])
        }
print("Inventario cargado correctamente.")
for id_producto, producto in inventario.items():
    print(
        "ID: ", id_producto,
        "Nombre: ", producto["nombre"],
        "Categoria: ", producto["categoria"],
        "Precio: ", producto["precio"],
        "Cantidad: ", producto["cantidad"]
    )

    def realizar_pedido(operador, id_producto, cantidad):
        with mutex:
            if id_producto not in inventario:
                print(operador, "- PRODUCTO NO ENCONTRADO")
                return
            
            producto = inventario[id_producto]
            print("Operador:", operador)
            print("Producto:", producto["nombre"])
            print("Cantidad solicitada", cantidad)
            print("Stock antes: ", producto["cantidad"])

            time.sleep(1)
            if cantidad < 0:
                print("Cantidad solicitada es incorrecta.")
            elif producto ["cantidad"] >= cantidad:
                producto["cantidad"] -= cantidad
                print("VENTA APROBADA")
                print("UNIDADES VENDIDAS:", cantidad)
                print("STOCK RESTANTE: ", producto["cantidad"])
            else:
                print("VENTA RECHAZADA")
                print("STOCK INSUFICIENTE")
                print("STOCK RESTANTE", producto["cantidad"])

h1 = threading.Thread(target=realizar_pedido, args=("Operador 1", 1, 20))
h2 = threading.Thread(target=realizar_pedido, args=("Operador 2", 1, 15))
h3 = threading.Thread(target=realizar_pedido, args=("Operador 3", 2, 30))
h4 = threading.Thread(target=realizar_pedido, args=("Operador 4", 1, 25))

h1.start()
h2.start()
h3.start()
h4.start()

h1.join()
h2.join()
h3.join()
h4.join()

print("INVENTARIO FINAL")
for id_producto, producto in inventario.items():
    print(
        "ID: ", id_producto,
        "Nombre: ", producto["nombre"],
        "Cantidad restante: ", producto["cantidad"]
    )

print("INVENTARIO FINAL")