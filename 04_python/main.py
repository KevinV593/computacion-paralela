import csv
import threading
import time

from conexion import conectar_mysql
import mysql.connector

id=[]
litros=[]

# r permiss de lectura
# newline cada linea
with open("datos.csv", "r",         #permisos de lectura, caracteres esp
          encoding="utf-8-sig", newline="") as archivo:
    lector = csv.reader(archivo)
    next(lector)
    for fila in lector:
        id.append(int (fila[0]))
        litros.append(float (fila[1]))
    print("Datos cargados correctamente")
    print("Numero de elementos cargados: ", len(id))

#por que len? 
mililitros = [0.0] * len(litros)
centilitros = [0.0] * len(litros)
metros_cubicos = [0.0] * len(litros)

def convertir_mililitros():
    #desde cero a 999
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

for i in range(len(id)):
    print("\n---------------")
    print("REGISTRO ", id[i])
    print("Litros = ",litros[i])
    print("Mililitros = ", mililitros[i])
    print("Centilitros = ", centilitros[i])
    print("Metros Cubicos = ", metros_cubicos[i])
    print("\n")
    
print("Primer Registro:", id[0] )
print("Ultimo Registro:", id[-1] )
print("TOTAL REGISTROS: ", len(id))

print(f"TIEMPO: {tiempo:.4f} ms")
    
#BASE DE DATOS

conexion = None
cursor = None

try:
    conexion = conectar_mysql()
    cursor = conexion.cursor()
    print("Conexión Exitosa a la base de datos MySQL")
    ### DUPLICATE ... actualiza el id
    sql_original = """
        INSERT INTO registros_litros (id, litros)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE litros = VALUES(litros)
    """
    #id y fechaprocsamiento ya se registrarn en auto
    sql_resultado = """
        INSERT INTO resultados_conversion
        (registro_id, mililitros, centilitros,
        metros_cubicos, tiempo_microsegundos)
        VALUES (%s, %s, %s, %s, %s)
    """
    for i in range(len(litros)):
        cursor.execute(sql_original, (id[i], litros[i]))
        cursor.execute(sql_resultado, (id[i], mililitros[i], centilitros[i], metros_cubicos[i], tiempo))
    conexion.commit()
    print("\n Datos Guardados CORRECTAMENTE")
    print("\n REGISTROS GUARDADOS = ", len(id))

except mysql.connector.Error as error:
    if conexion is not None:
        conexion.rollback()
    print(f"Error al guardar datos: {error}")
    
finally:
    if cursor is not None:
        cursor.close()
    if cursor is not None and conexion.is_connected():
        conexion.close()