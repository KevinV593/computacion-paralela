
import streamlit as st
import pandas as pd
import plotly.express as px
import threading
import time

# ==========================================
# 1. CONFIGURACION DEL DASHBOARD
# ==========================================

st.set_page_config(
    page_title="Dashboard Climatico",
    page_icon="🌤️",
    layout="wide"
)

st.title("Dashboard de Prediccion Climatica")
st.caption("Computacion Paralela | Python + Streamlit + Threading")


# ==========================================
# 2. CARGAR DATASET
# ==========================================

def cargar_datos():

    datos = pd.read_csv("clima_5000.csv")

    columnas = [
        "hora",
        "temperatura",
        "humedad",
        "presion",
        "viento"
    ]

    if not all(columna in datos.columns for columna in columnas):
        raise ValueError("El CSV no contiene todas las columnas requeridas.")

    datos = datos[columnas].copy()

    for columna in columnas:
        datos[columna] = pd.to_numeric(
            datos[columna],
            errors="raise"
        )

    if datos.isnull().any().any():
        raise ValueError("El dataset contiene valores vacios.")

    if len(datos) < 24:
        raise ValueError("Se necesitan al menos 24 registros.")

    datos = datos.sort_values("hora").reset_index(drop=True)

    if datos["hora"].duplicated().any():
        raise ValueError("Existen horas duplicadas en el dataset.")

    return datos


# ==========================================
# 3. CARGAR Y VALIDAR REGISTROS
# ==========================================

try:
    datos = cargar_datos()

except Exception as error:
    st.error(f"Error al cargar dataset: {error}")
    st.stop()

st.success("Dataset cargado correctamente.")


# ==========================================
# 4. FILTROS INTERACTIVOS
# ==========================================

st.sidebar.header("Configuracion de prediccion")

horas_futuras = st.sidebar.slider(
    "Numero de horas a futuro",
    min_value=24,
    max_value=72,
    value=72,
    step=1
)

ciclos_dia = st.sidebar.selectbox(
    "Ciclos del dia",
    options=[1, 2, 3],
    index=2
)

horas_ciclo = st.sidebar.selectbox(
    "Horas a calcular por ciclo",
    options=[6, 12, 24],
    index=2
)

st.sidebar.info(
    f"Prediccion configurada para {horas_futuras} horas."
)


# ==========================================
# 5. FUNCION DE PREDICCION
# ==========================================

semaforo = threading.Semaphore(2)
mutex = threading.Lock()

resultados = []
tiempos = {}

def predecir(variable, hora_objetivo):

    registros = datos[
        datos["hora"] % 24 == hora_objetivo % 24
    ][variable]

    if registros.empty:
        raise ValueError(
            f"No existen registros historicos para {variable}."
        )

    return registros.mean()


# ==========================================
# 6. FUNCIONES DE LOS CUATRO HILOS
# ==========================================

def procesar_variable(variable):

    inicio = time.perf_counter()

    with semaforo:

        predicciones = []

        for hora in range(
            int(datos["hora"].max()) + 1,
            int(datos["hora"].max()) + 1 + horas_futuras
        ):

            valor = predecir(variable, hora)

            predicciones.append({
                "hora_futura": hora,
                "ciclo": ((hora - int(datos["hora"].max()) - 1) // 24) + 1,
                "hora_dia": hora % 24,
                "variable": variable,
                "prediccion": round(float(valor), 2)
            })

        fin = time.perf_counter()

        with mutex:

            resultados.extend(predicciones)

            tiempos[variable] = round(
                fin - inicio, 4
            )


# ==========================================
# 7. EJECUCION DE LOS CUATRO HILOS
# ==========================================

if st.button("Ejecutar prediccion climatica", type="primary"):

    resultados = []
    tiempos = {}

    inicio_total = time.perf_counter()

    variables = [
        "temperatura",
        "humedad",
        "presion",
        "viento"
    ]

    hilos = []

    for variable in variables:

        hilo = threading.Thread(
            target=procesar_variable,
            args=(variable,)
        )

        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    fin_total = time.perf_counter()

    tiempo_total = round(
        fin_total - inicio_total, 4
    )

    df_resultados = pd.DataFrame(resultados)

    df_resultados = df_resultados.sort_values(
        ["hora_futura", "variable"]
    ).reset_index(drop=True)

    st.session_state["resultados"] = df_resultados
    st.session_state["tiempos"] = tiempos
    st.session_state["tiempo_total"] = tiempo_total

    st.success("Prediccion climatica completada correctamente.")


# ==========================================
# 8. RECUPERAR RESULTADOS
# ==========================================

if "resultados" not in st.session_state:

    st.info(
        "Configure los parametros y presione "
        "'Ejecutar prediccion climatica'."
    )

    st.stop()

resultados_df = st.session_state["resultados"]
tiempos = st.session_state["tiempos"]
tiempo_total = st.session_state["tiempo_total"]


# ==========================================
# 9. INDICADORES GENERALES
# ==========================================

st.subheader("Indicadores generales")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Registros historicos",
    len(datos)
)

col2.metric(
    "Hilos utilizados",
    4
)

col3.metric(
    "Horas predichas",
    horas_futuras
)

col4.metric(
    "Tiempo de ejecucion",
    f"{tiempo_total:.4f} s"
)


# ==========================================
# 10. GRAFICOS DE PREDICCION
# ==========================================

st.subheader("Predicciones climaticas")

nombres = {
    "temperatura": "Temperatura (°C)",
    "humedad": "Humedad (%)",
    "presion": "Presion (hPa)",
    "viento": "Viento (m/s)"
}

for variable, titulo in nombres.items():

    df_variable = resultados_df[
        resultados_df["variable"] == variable
    ]

    fig = px.line(
        df_variable,
        x="hora_futura",
        y="prediccion",
        color="ciclo",
        markers=True,
        title=titulo
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================
# 11. ANALISIS DE TIEMPOS
# ==========================================

st.subheader("Tiempo de procesamiento por hilo")

df_tiempos = pd.DataFrame({
    "Variable": list(tiempos.keys()),
    "Tiempo (segundos)": list(tiempos.values())
})

fig_tiempo = px.bar(
    df_tiempos,
    x="Variable",
    y="Tiempo (segundos)",
    color="Variable",
    title="Tiempo de procesamiento de cada hilo"
)

st.plotly_chart(
    fig_tiempo,
    use_container_width=True
)

st.caption(
    f"Tiempo total de ejecucion concurrente: {tiempo_total:.4f} segundos."
)


# ==========================================
# 12. TABLA INTERACTIVA
# ==========================================

st.subheader("Resultados de prediccion")

ciclo_seleccionado = st.selectbox(
    "Seleccionar ciclo",
    options=sorted(resultados_df["ciclo"].unique())
)

tabla = resultados_df[
    resultados_df["ciclo"] == ciclo_seleccionado
]

st.dataframe(
    tabla,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 13. DESCARGAR RESULTADOS
# ==========================================

csv = resultados_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    "Descargar predicciones CSV",
    data=csv,
    file_name="predicciones_climaticas.csv",
    mime="text/csv"
)
