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

#EJECICIO 
h1 = threading.Thread(target=realizar_pedido, args=("Operador 1", 2, 50))
h2 = threading.Thread(target=realizar_pedido, args=("Operador 2", 2, 50))
h3 = threading.Thread(target=realizar_pedido, args=("Operador 3", 2, 50))

h4 = threading.Thread(target=realizar_pedido, args=("Operador 4", 5, 20))
h5 = threading.Thread(target=realizar_pedido, args=("Operador 5", 5, 10))
h6 = threading.Thread(target=realizar_pedido, args=("Operador 6", 5, 30))

h7 = threading.Thread(target=realizar_pedido, args=("Operador 7", 8, 15))
h8 = threading.Thread(target=realizar_pedido, args=("Operador 8", 8, 15))
h9 = threading.Thread(target=realizar_pedido, args=("Operador 9", 8, 15))

h1.start()
h2.start()
h3.start()
h4.start()
h5.start()
h6.start()
h7.start()
h8.start()
h9.start()

h1.join()
h2.join()
h3.join()
h4.join()
h5.join()
h6.join()
h7.join()
h8.join()
h9.join()

print("INVENTARIO FINAL")
for id_producto, producto in inventario.items():
    print(
        "ID: ", id_producto,
        "Nombre: ", producto["nombre"],
        "Cantidad restante: ", producto["cantidad"]
    )

print("INVENTARIO FINAL")


#CARGAR 10 HILOS U OPERADORES DONDE:
# LOS PRIMEROS TRES OPERADORES 
# Operador 1, id 2, 50 cantidades solcitadas
# Operador 2, id 2, 50
# Operador 3, id 2, 50
# Operador 4 5 6: id 5
# op4 20 cantidades
# op5 10 unicades
# op6 30 cant
#Operador 7, 8 y 9 ingresan al id 8
#solictan 15 productos