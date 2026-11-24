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

    horas_futuras = 48
    semaforo = threading.Semaphore(2)
    mutex = threading.Lock()
    resultados = {}

    def predecir (variable, horas):
        hora_objetivo = datos[-1]["hora"] + horas
        registros = []

        for fila in datos:
            if fila["hora"] % 24 == hora_objetivo % 24:
                registros.append(fila[variable])

        if not registros:
            raise ValueError(f"No se encontraron registros para la hora {hora_objetivo}.")

        promedio = sum(registros) / len(registros)
        return promedio

    #funciones del primer hilo
    def hilo_temperatura():
        with semaforo:
            temperatura = predecir("temperatura", horas_futuras)
            time.sleep(2) # espera dos segundos
            with mutex:
                resultados["temperatura"] = round(temperatura, 2)
                print(f"H1: Predicción de temperatura para dentro de {horas_futuras} horas: {resultados['temperatura']} °C")

    #funciones del segundo hilo
    def hilo_humedad():
        with semaforo:
            humedad = predecir("humedad", horas_futuras)
            time.sleep(2) # espera dos segundos
            with mutex:
                resultados["humedad"] = round(humedad, 2)
                print(f"H2: Predicción de humedad para dentro de {horas_futuras} horas: {resultados['humedad']} %")

    #funciones del tercer hilo
    def hilo_presion():
        with semaforo:
            presion = predecir("presion", horas_futuras)
            time.sleep(2) # espera dos segundos
            with mutex:
                resultados["presion"] = round(presion, 2)
                print(f"H3: Predicción de presión para dentro de {horas_futuras} horas: {resultados['presion']} hPa")

    #funciones del cuarto hilo
    def hilo_viento():
        with semaforo:
            viento = predecir("viento", horas_futuras)
            time.sleep(2) # espera dos segundos
            with mutex:
                resultados["viento"] = round(viento, 2)
                print(f"H4: Predicción de viento para dentro de {horas_futuras} horas: {resultados['viento']} m/s")

    inicio = time.perf_counter()

    h1 = threading.Thread(target=hilo_temperatura)
    h2 = threading.Thread(target=hilo_humedad)
    h3 = threading.Thread(target=hilo_presion)
    h4 = threading.Thread(target=hilo_viento)

    h1.start()
    h2.start()
    h3.start()
    h4.start()

    h1.join()
    h2.join()
    h3.join()
    h4.join()

    fin = time.perf_counter()
    print(f"\nPrediccion Climatica")
    print(f"Horas Futuras: {horas_futuras}")
    print("Temperatura: ", resultados["temperatura"], "°C")
    print("Humedad: ", resultados["humedad"], "%")
    print("Presion: ", resultados["presion"], "hPa")
    print("Viento: ", resultados["viento"], "m/s")

    print(f"Tiempo de ejecución: {round(fin - inicio, 2)} segundos")

#PREDECIR 21 HORAS despues de la Hora 48
#PREDECIR 72 HORAS despues del ultimo registro