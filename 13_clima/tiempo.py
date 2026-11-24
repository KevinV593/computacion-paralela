import csv
import threading
import time
from pathlib import Path

# ---------------------------------------------------------
# CONFIGURACION DEL ESCENARIO DE PREDICCION
# ---------------------------------------------------------
ARCHIVO_CSV = "clima_5000.csv"

# -1 = ultimo registro disponible.
#  0 = primer registro.
# 48 = registro en la posicion 48 (indice de Python).
INDICE_REFERENCIA = -1

# Horas que se suman a la hora del registro de referencia.
HORAS_FUTURAS = 48

# 24 = comparar la misma hora de cada dia.
CICLO_HISTORICO = 24

MAX_HILOS_SIMULTANEOS = 2

# Se conserva la pausa del programa original.
# Cambiar a 0 si no se necesita simular tiempo de trabajo.
PAUSA_SIMULADA_SEGUNDOS = 2

VARIABLES = {
    "temperatura": {"etiqueta": "Temperatura", "unidad": "°C"},
    "humedad": {"etiqueta": "Humedad", "unidad": "%"},
    "presion": {"etiqueta": "Presión", "unidad": "hPa"},
    "viento": {"etiqueta": "Viento", "unidad": "m/s"},
}


def cargar_datos(ruta_csv=ARCHIVO_CSV):
    """Lee el CSV y devuelve una lista de registros meteorológicos."""
    datos = []

    with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        columnas = {"hora", *VARIABLES.keys()}

        if not lector.fieldnames or not columnas.issubset(lector.fieldnames):
            raise ValueError(
                "El CSV debe contener: hora, temperatura, humedad, presion y viento."
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


def obtener_referencia(datos, indice=INDICE_REFERENCIA):
    """Devuelve el registro de referencia y su índice real."""
    try:
        registro = datos[indice]
    except IndexError as error:
        raise IndexError(
            f"El índice {indice} no existe. El CSV contiene {len(datos)} registros."
        ) from error

    indice_real = indice if indice >= 0 else len(datos) + indice
    return registro, indice_real


def predecir(datos, variable, hora_objetivo, ciclo=CICLO_HISTORICO):
    """
    Calcula el promedio de la variable usando todos los registros
    cuya hora coincide con la hora objetivo dentro del ciclo indicado.

    Devuelve el promedio y los registros que participaron en el cálculo.
    """
    if ciclo <= 0:
        raise ValueError("El ciclo histórico debe ser mayor que cero.")

    registros = [
        fila for fila in datos
        if fila["hora"] % ciclo == hora_objetivo % ciclo
    ]

    if not registros:
        raise ValueError(
            f"No se encontraron registros para la hora objetivo {hora_objetivo}."
        )

    valores = [fila[variable] for fila in registros]
    promedio = sum(valores) / len(valores)

    detalle = [
        {"hora": fila["hora"], "valor": fila[variable]}
        for fila in registros
    ]

    return promedio, detalle


def ejecutar_predicciones(
    datos,
    indice_referencia=INDICE_REFERENCIA,
    horas_futuras=HORAS_FUTURAS,
    ciclo_historico=CICLO_HISTORICO,
):
    """
    Ejecuta las cuatro predicciones en hilos y devuelve:
    - configuración efectiva,
    - resultados de cada variable y registros utilizados,
    - tiempo total de ejecución.
    """
    registro_ref, indice_real = obtener_referencia(datos, indice_referencia)
    hora_referencia = registro_ref["hora"]
    hora_objetivo = hora_referencia + horas_futuras

    semaforo = threading.Semaphore(MAX_HILOS_SIMULTANEOS)
    mutex = threading.Lock()
    resultados = {}
    errores = {}

    def trabajador(variable):
        try:
            with semaforo:
                promedio, registros = predecir(
                    datos, variable, hora_objetivo, ciclo_historico
                )

                if PAUSA_SIMULADA_SEGUNDOS > 0:
                    time.sleep(PAUSA_SIMULADA_SEGUNDOS)

                with mutex:
                    resultados[variable] = {
                        "valor": round(promedio, 2),
                        "registros_utilizados": registros,
                        "cantidad_registros": len(registros),
                    }
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
        raise RuntimeError(f"No se pudieron completar las predicciones: {errores}")

    referencia_texto = (
        "Último registro" if indice_referencia == -1
        else f"Posición {indice_real}"
    )

    configuracion = {
        "indice_referencia_configurado": indice_referencia,
        "indice_referencia_real": indice_real,
        "referencia_texto": referencia_texto,
        "hora_referencia": hora_referencia,
        "horas_futuras": horas_futuras,
        "hora_objetivo": hora_objetivo,
        "ciclo_historico": ciclo_historico,
        "total_registros": len(datos),
        "max_hilos_simultaneos": MAX_HILOS_SIMULTANEOS,
        "cantidad_hilos": len(VARIABLES),
    }

    return {
        "configuracion": configuracion,
        "predicciones": resultados,
        "tiempo_ejecucion_segundos": tiempo_ejecucion,
    }


def main():
    datos = cargar_datos()
    resultado = ejecutar_predicciones(datos)

    print(f"Registros totales: {len(datos)}")
    print("\nPredicción climática")
    print(
        f"Referencia: {resultado['configuracion']['referencia_texto']} "
        f"(hora {resultado['configuracion']['hora_referencia']})"
    )
    print(f"Horizonte: {HORAS_FUTURAS} horas")
    print(f"Ciclo histórico: {CICLO_HISTORICO} horas")

    for variable, info in VARIABLES.items():
        valor = resultado["predicciones"][variable]["valor"]
        print(f"{info['etiqueta']}: {valor} {info['unidad']}")

    print(f"Tiempo de ejecución: {resultado['tiempo_ejecucion_segundos']} segundos")


# Al importar tiempo.py desde el dashboard, main() NO se ejecuta.
# Solo se ejecuta cuando se lanza directamente: python tiempo.py
if __name__ == "__main__":
    main()
