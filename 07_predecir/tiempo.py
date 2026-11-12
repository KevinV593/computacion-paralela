import csv
import threading
import time

#cargar datos

datos = []

with open("clima_5000.csv", "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        datos.append({
            "hora": int(fila["hora"]),
            "temperatura": float(fila["temperatura"]),
            "humedad": float(fila["humedad"]),
            "presion": float(fila["presion"]),
            "viento": float(fila["viento"])
        })
    print("Registros Totales: ", len(datos))
    
    if len(datos) < 24:
        raise ValueError("Al menos debe tener 24 registros: ")

    horas