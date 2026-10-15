import csv
import threading
import time

from conexion import conectar_mysql
import mysql.connector

id=[]
litros=[]

# r permiss de lectura
# newline cada linea
with open("datos.csv", "r",
          encoding="utf-8-sig", newline="") as archivo:
    lector = csv.reader(archivo)
    next(lector)
    for fila in lector:
        id.append(fila[0])
        litros.append(fila[1])
        
    print("Datos cargados correctamente")
    print("Numero de elementos cargados: ", len(id))

#por que len?
mililitros = [0.0] * len(litros)
centilitros = [0.0] * len(litros)
metros_cubicos = [0.0] * len(litros)

def convertir_mililitros():
    #desde cero
    for i in range(len(litros)):
        mililitros[i] = litros[i] * 1000

def convertir_centilitros():
    #desde cero
    for i in range(len(litros)):
        centilitros[i] = litros[i] * 100

def convertir_metroCubico():
    #desde cero
    for i in range(len(litros)):
        metros_cubicos[i] = litros[i] / 1000

h1 = threading.Thread(target=convertir_mililitros)
h2 = threading.Thread(target=convertir_centilitros)
h3 = threading.Thread(target=convertir_metroCubico)

inicio = time.perf_counter_ns()

h1.start()
h2.start()
h3.start()

h1.join()
h2.join()
h3.join()

fin = time.perf_counter_ns()
tiempo = (fin - inicio) / 1000000 #milisengundos

for i in range (len(id)):
    print("\n---------------")
    print("REGISTRO ", id[i])
    print("Litros = ",litros[i])
    print("Mililitros = ", mililitros[i])
    print("Centilitros = ", centilitros[i])
    print("Metros Cubicos = ", metros_cubicos[i])
    print("\n")
    print(f"TIEMPO: {tiempo:.4f} ms")
