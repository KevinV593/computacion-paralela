import csv
import json
import threading
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------
# CONFIGURACION DEL ESCENARIO DE PREDICCION CLIMATICA
# ---------------------------------------------------------
ARCHIVO_CSV = "clima_5000.csv"
ARCHIVO_RESULTADOS = "resultados_clima.json"

# Registro de referencia:
# -1 = ultimo registro disponible.
#  0 = primer registro.
# 48 = registro ubicado en la posicion 48 (indice de Python).
INDICE_REFERENCIA = -1

# Cantidad de horas posteriores al registro de referencia.
HORAS_FUTURAS = 48

# Ciclo historico utilizado para seleccionar registros equivalentes.
# 24 = mismo horario de cada dia.
CICLO_HISTORICO = 24

# Limita la cantidad de hilos que pueden ejecutar simultaneamente
# la seccion protegida por el semaforo.
MAX_HILOS_SIMULTANEOS = 2

# Se conserva la pausa del programa original. Sirve para simular
# tiempo de trabajo; no forma parte del calculo meteorologico.
PAUSA_SIMULADA_SEGUNDOS = 2

VARIABLES = {
    "temperatura": {"unidad": "°C", "etiqueta": "Temperatura"},
    "humedad": {"unidad": "%", "etiqueta": "Humedad"},
    "presion": {"unidad": "hPa", "etiqueta": "Presión"},
    "viento": {"unidad": "m/s", "etiqueta": "Viento"},
}


def cargar_datos(ruta_csv):
    datos = []
    with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        columnas_requeridas = {"hora", *VARIABLES.keys()}

        if not lector.fieldnames or not columnas_requeridas.issubset(lector.fieldnames):
            raise ValueError(
                "El CSV debe contener las columnas: hora, temperatura, "
                "humedad, presion y viento."
            )

        for fila in lector:
            datos.append({
                "hora": int(fila["hora"]),
                "temperatura": float(fila["temperatura"]),
                "humedad": float(fila["humedad"]),
                "presion": float(fila["presion"]),
                "viento": float(fila["viento"]),
            })

    if len(datos) < 24:
        raise ValueError("El archivo debe contener al menos 24 registros.")

    return datos


def obtener_registro_referencia(datos, indice):
    try:
        registro = datos[indice]
    except IndexError as error:
        raise IndexError(
            f"El indice de referencia {indice} no existe. "
            f"El CSV contiene {len(datos)} registros."
        ) from error

    indice_real = indice if indice >= 0 else len(datos) + indice
    return registro, indice_real


def calcular_prediccion(datos, variable, hora_objetivo, ciclo):
    registros_utilizados = [
        fila for fila in datos
        if fila["hora"] % ciclo == hora_objetivo % ciclo
    ]

    if not registros_utilizados:
        raise ValueError(
            f"No se encontraron registros para la hora objetivo {hora_objetivo}."
        )

    valores = [fila[variable] for fila in registros_utilizados]
    promedio = sum(valores) / len(valores)

    detalle = [
        {"hora": fila["hora"], "valor": fila[variable]}
        for fila in registros_utilizados
    ]

    return promedio, detalle


def ejecutar_predicciones(datos, hora_objetivo):
    semaforo = threading.Semaphore(MAX_HILOS_SIMULTANEOS)
    mutex = threading.Lock()
    resultados = {}
    errores = {}

    def trabajador(variable):
        try:
            with semaforo:
                promedio, registros = calcular_prediccion(
                    datos, variable, hora_objetivo, CICLO_HISTORICO
                )
                time.sleep(PAUSA_SIMULADA_SEGUNDOS)

                with mutex:
                    resultados[variable] = {
                        "valor": round(promedio, 2),
                        "registros_utilizados": registros,
                        "cantidad_registros": len(registros),
                    }
                    print(
                        f"{VARIABLES[variable]['etiqueta']}: "
                        f"{resultados[variable]['valor']} "
                        f"{VARIABLES[variable]['unidad']}"
                    )
        except Exception as error:
            with mutex:
                errores[variable] = str(error)

    hilos = [
        threading.Thread(target=trabajador, args=(variable,))
        for variable in VARIABLES
    ]

    inicio = time.perf_counter()

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    tiempo_ejecucion = round(time.perf_counter() - inicio, 4)

    if errores:
        raise RuntimeError(f"Error al calcular predicciones: {errores}")

    return resultados, tiempo_ejecucion


def main():
    ruta_csv = Path(ARCHIVO_CSV)
    if not ruta_csv.exists():
        raise FileNotFoundError(
            f"No se encontro '{ARCHIVO_CSV}'. Coloca el CSV en la misma "
            "carpeta que tiempo.py o ajusta ARCHIVO_CSV."
        )

    datos = cargar_datos(ruta_csv)
    registro_referencia, indice_real = obtener_registro_referencia(
        datos, INDICE_REFERENCIA
    )

    hora_objetivo = registro_referencia["hora"] + HORAS_FUTURAS

    print(f"Registros totales: {len(datos)}")
    print(f"Hora del registro de referencia: {registro_referencia['hora']}")
    print(f"Hora objetivo: {hora_objetivo}")

    resultados, tiempo_ejecucion = ejecutar_predicciones(datos, hora_objetivo)

    referencia_texto = (
        "Último registro" if INDICE_REFERENCIA == -1
        else f"Posición {indice_real}"
    )

    salida = {
        "generado_en": datetime.now().astimezone().isoformat(timespec="seconds"),
        "archivo_csv": str(ruta_csv),
        "configuracion": {
            "indice_referencia_configurado": INDICE_REFERENCIA,
            "indice_referencia_real": indice_real,
            "referencia_texto": referencia_texto,
            "hora_referencia": registro_referencia["hora"],
            "horas_futuras": HORAS_FUTURAS,
            "hora_objetivo": hora_objetivo,
            "ciclo_historico": CICLO_HISTORICO,
            "total_registros": len(datos),
            "max_hilos_simultaneos": MAX_HILOS_SIMULTANEOS,
            "cantidad_hilos": len(VARIABLES),
        },
        "predicciones": resultados,
        "rendimiento": {
            "tiempo_ejecucion_segundos": tiempo_ejecucion,
            "pausa_simulada_segundos_por_hilo": PAUSA_SIMULADA_SEGUNDOS,
        },
    }

    with open(ARCHIVO_RESULTADOS, "w", encoding="utf-8") as archivo:
        json.dump(salida, archivo, ensure_ascii=False, indent=4)

    print("\nPredicción climática finalizada.")
    print(f"Resultados guardados en: {ARCHIVO_RESULTADOS}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")


if __name__ == "__main__":
    main()
