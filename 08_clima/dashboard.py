import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# CONFIGURACION DEL DASHBOARD
# ---------------------------------------------------------
ARCHIVO_CSV = "clima_5000.csv"
ARCHIVO_RESULTADOS = "resultados_clima.json"

VARIABLES = {
    "Temperatura": {"columna": "temperatura", "unidad": "°C", "icono": "🌡️"},
    "Humedad": {"columna": "humedad", "unidad": "%", "icono": "💧"},
    "Presión": {"columna": "presion", "unidad": "hPa", "icono": "🌫️"},
    "Viento": {"columna": "viento", "unidad": "m/s", "icono": "💨"},
}

st.set_page_config(
    page_title="Dashboard meteorológico",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def cargar_csv(ruta):
    df = pd.read_csv(ruta)
    columnas = ["hora", "temperatura", "humedad", "presion", "viento"]
    faltantes = [col for col in columnas if col not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el CSV: {', '.join(faltantes)}")
    return df[columnas].copy()


def cargar_resultados(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def formato_numero(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def filtrar_periodo(df, periodo):
    if df.empty:
        return df

    ultima_hora = df["hora"].max()
    if periodo == "Últimas 24 horas":
        minimo = ultima_hora - 23
    elif periodo == "Últimos 7 días":
        minimo = ultima_hora - (7 * 24 - 1)
    elif periodo == "Últimos 30 días":
        minimo = ultima_hora - (30 * 24 - 1)
    else:
        minimo = df["hora"].min()

    return df[df["hora"] >= minimo].copy()


def reducir_puntos(df, max_puntos=1200):
    if len(df) <= max_puntos:
        return df
    posiciones = pd.Series(range(len(df))).iloc[
        ::max(1, len(df) // max_puntos)
    ].tolist()
    if posiciones[-1] != len(df) - 1:
        posiciones.append(len(df) - 1)
    return df.iloc[posiciones].copy()


# ---------------------------------------------------------
# CARGA DE INFORMACION
# ---------------------------------------------------------
st.title("🌤️ Dashboard meteorológico")
st.caption("Monitoreo histórico y análisis de predicciones climáticas")

ruta_csv = Path(ARCHIVO_CSV)
ruta_resultados = Path(ARCHIVO_RESULTADOS)

if not ruta_csv.exists() or not ruta_resultados.exists():
    st.error(
        "No se encontraron los archivos necesarios. Ejecuta primero "
        "`tiempo.py` y verifica que `clima_5000.csv` esté en esta carpeta."
    )
    st.stop()

try:
    df = cargar_csv(str(ruta_csv))
    datos_resultado = cargar_resultados(ruta_resultados)
except Exception as error:
    st.error(f"No fue posible cargar la información: {error}")
    st.stop()

config = datos_resultado["configuracion"]
predicciones = datos_resultado["predicciones"]
rendimiento = datos_resultado["rendimiento"]

# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------
with st.sidebar:
    st.header("Controles")
    if st.button("🔄 Actualizar datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    variable_seleccionada = st.selectbox(
        "Variable climática",
        list(VARIABLES.keys()),
        index=0,
    )

    periodo = st.selectbox(
        "Período histórico",
        [
            "Últimas 24 horas",
            "Últimos 7 días",
            "Últimos 30 días",
            "Todo el histórico",
        ],
        index=1,
    )

    st.divider()
    st.caption("Datos de origen")
    st.write(f"**Archivo:** {ARCHIVO_CSV}")
    st.write(f"**Registros:** {len(df):,}".replace(",", "."))

# ---------------------------------------------------------
# 1. INSTRUCCION DE PREDICCION
# ---------------------------------------------------------
st.subheader("Instrucción de predicción")

referencia = config["referencia_texto"]
horas = config["horas_futuras"]
ciclo = config["ciclo_historico"]

st.info(
    f"Predecir **{horas} horas** después del **{referencia.lower()}**, "
    f"utilizando un ciclo histórico de **{ciclo} horas**."
)

col_a, col_b, col_c = st.columns(3)
col_a.metric("Registro de referencia", referencia)
col_b.metric("Horizonte de predicción", f"{horas} horas")
col_c.metric("Ciclo histórico", f"{ciclo} horas")

# ---------------------------------------------------------
# 2. TARJETAS DE PREDICCION
# ---------------------------------------------------------
st.subheader("Resultados de la predicción")

columnas = st.columns(4)
for columna, (clave, info) in zip(columnas, VARIABLES.items()):
    nombre_json = info["columna"]
    resultado = predicciones[nombre_json]
    valor = resultado["valor"]
    columna.metric(
        label=f"{info['icono']} {clave}",
        value=f"{formato_numero(valor)} {info['unidad']}",
        help=(
            f"Calculado a partir de {resultado['cantidad_registros']} "
            "registros históricos coincidentes."
        ),
    )

# ---------------------------------------------------------
# 3. COMPORTAMIENTO HISTORICO
# ---------------------------------------------------------
st.divider()
st.subheader("Comportamiento histórico")
st.caption(
    "Explora una variable a la vez. El filtro temporal evita mostrar "
    "innecesariamente todos los registros."
)

info_variable = VARIABLES[variable_seleccionada]
columna = info_variable["columna"]
unidad = info_variable["unidad"]

df_periodo = filtrar_periodo(df, periodo)
df_grafica = reducir_puntos(df_periodo)

fig_historico = px.line(
    df_grafica,
    x="hora",
    y=columna,
    markers=False,
    labels={"hora": "Hora del registro", columna: f"{variable_seleccionada} ({unidad})"},
)
fig_historico.update_traces(line=dict(width=2))
fig_historico.update_layout(
    template="plotly_white",
    height=390,
    margin=dict(l=15, r=15, t=25, b=15),
    hovermode="x unified",
)
st.plotly_chart(fig_historico, use_container_width=True)

st.caption(
    f"Mostrando {len(df_grafica):,} puntos de {len(df_periodo):,} registros "
    f"del período seleccionado.".replace(",", ".")
)

# ---------------------------------------------------------
# 4. REGISTROS QUE PARTICIPARON EN LA PREDICCION
# ---------------------------------------------------------
st.divider()
st.subheader("Análisis de la predicción")
st.caption(
    "Estos son los registros históricos que tiempo.py seleccionó realmente "
    "para calcular el promedio de la variable elegida."
)

resultado_variable = predicciones[columna]
registros = resultado_variable["registros_utilizados"]
df_origen = pd.DataFrame(registros)

if not df_origen.empty:
    df_origen = df_origen.sort_values("hora")
    promedio = resultado_variable["valor"]

    fig_origen = px.bar(
        df_origen,
        x="hora",
        y="valor",
        labels={"hora": "Hora histórica", "valor": f"{variable_seleccionada} ({unidad})"},
        hover_data={"hora": True, "valor": ":.2f"},
    )
    fig_origen.add_hline(
        y=promedio,
        line_dash="dash",
        line_width=2,
        annotation_text=f"Promedio pronosticado: {formato_numero(promedio)} {unidad}",
        annotation_position="top left",
    )
    fig_origen.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=15, r=15, t=45, b=15),
        showlegend=False,
    )
    st.plotly_chart(fig_origen, use_container_width=True)

    with st.expander("Consultar registros utilizados"):
        tabla = df_origen.rename(
            columns={"hora": "Hora del registro", "valor": f"Valor ({unidad})"}
        )
        st.dataframe(tabla, use_container_width=True, hide_index=True)

    st.success(
        f"La predicción de {variable_seleccionada.lower()} se obtuvo "
        f"promediando {len(df_origen)} registros históricos."
    )
else:
    st.warning("El archivo de resultados no contiene registros para esta variable.")

# ---------------------------------------------------------
# 5. INFORMACION DE RENDIMIENTO
# ---------------------------------------------------------
st.divider()
st.subheader("Información de ejecución")

r1, r2, r3 = st.columns(3)
r1.metric(
    "Tiempo de ejecución",
    f"{formato_numero(rendimiento['tiempo_ejecucion_segundos'])} s",
)
r2.metric("Registros procesados", f"{config['total_registros']:,}".replace(",", "."))
r3.metric(
    "Hilos simultáneos permitidos",
    f"{config['max_hilos_simultaneos']} de {config['cantidad_hilos']}",
)

st.caption(
    f"Resultados generados: {datos_resultado.get('generado_en', 'No disponible')} "
    "· El dashboard presenta el último archivo de resultados generado por tiempo.py."
)
