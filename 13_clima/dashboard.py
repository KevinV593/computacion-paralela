from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import tiempo

ARCHIVO_CSV = tiempo.ARCHIVO_CSV

VARIABLES_UI = {
    "Temperatura": {"clave": "temperatura", "unidad": "°C", "icono": "🌡️"},
    "Humedad": {"clave": "humedad", "unidad": "%", "icono": "💧"},
    "Presión": {"clave": "presion", "unidad": "hPa", "icono": "🌫️"},
    "Viento": {"clave": "viento", "unidad": "m/s", "icono": "💨"},
}

st.set_page_config(
    page_title="Dashboard meteorológico",
    page_icon="🌤️",
    layout="wide",
)

st.title("🌤️ Dashboard meteorológico")
st.caption("Visualización histórica y análisis de predicciones climáticas")


@st.cache_data(show_spinner=False)
def cargar_csv(ruta):
    df = pd.read_csv(ruta)
    columnas = ["hora", "temperatura", "humedad", "presion", "viento"]
    faltantes = [col for col in columnas if col not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el CSV: {', '.join(faltantes)}")
    return df[columnas].copy()


@st.cache_data(show_spinner="Ejecutando las predicciones...")
def obtener_predicciones(ruta_csv, indice, horizonte, ciclo):
    # La lógica de predicción está en tiempo.py.
    # Streamlit conserva en caché el resultado para no repetir los hilos
    # cada vez que el usuario cambia un selector de las gráficas.
    datos = tiempo.cargar_datos(ruta_csv)
    return tiempo.ejecutar_predicciones(
        datos,
        indice_referencia=indice,
        horas_futuras=horizonte,
        ciclo_historico=ciclo,
    )


def filtrar_periodo(df, periodo):
    ultima_hora = df["hora"].max()

    if periodo == "Últimas 24 horas":
        inicio = ultima_hora - 23
    elif periodo == "Últimos 7 días":
        inicio = ultima_hora - (7 * 24 - 1)
    elif periodo == "Últimos 30 días":
        inicio = ultima_hora - (30 * 24 - 1)
    else:
        inicio = df["hora"].min()

    return df[df["hora"] >= inicio].copy()


def reducir_puntos(df, max_puntos=1200):
    """Reduce puntos solo para dibujar; no modifica los datos ni predicciones."""
    if len(df) <= max_puntos:
        return df

    paso = max(1, len(df) // max_puntos)
    reducido = df.iloc[::paso].copy()

    if reducido.iloc[-1]["hora"] != df.iloc[-1]["hora"]:
        reducido = pd.concat([reducido, df.iloc[[-1]]])

    return reducido


def formato_numero(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


ruta_csv = Path(ARCHIVO_CSV)
if not ruta_csv.exists():
    st.error(
        f"No se encontró {ARCHIVO_CSV}. Coloca el CSV en la misma carpeta "
        "que tiempo.py y dashboard.py."
    )
    st.stop()

# ---------------------------------------------------------
# SIDEBAR: filtros de visualización y actualización
# ---------------------------------------------------------
with st.sidebar:
    st.header("Controles")

    if st.button("🔄 Volver a ejecutar predicción", use_container_width=True):
        obtener_predicciones.clear()
        st.rerun()

    variable_nombre = st.selectbox("Variable climática", list(VARIABLES_UI))
    periodo = st.selectbox(
        "Período histórico",
        ["Últimas 24 horas", "Últimos 7 días", "Últimos 30 días", "Todo el histórico"],
        index=1,
    )

    st.divider()
    st.caption("Los filtros de las gráficas no vuelven a ejecutar la predicción.")

# Carga de histórico y cálculo compartido desde tiempo.py
try:
    df = cargar_csv(str(ruta_csv))
    # El dashboard utiliza los mismos parámetros definidos en tiempo.py.
    resultado = obtener_predicciones(
        str(ruta_csv),
        tiempo.INDICE_REFERENCIA,
        tiempo.HORAS_FUTURAS,
        tiempo.CICLO_HISTORICO,
    )
except Exception as error:
    st.error(f"No se pudo procesar la información: {error}")
    st.stop()

config = resultado["configuracion"]
predicciones = resultado["predicciones"]

# ---------------------------------------------------------
# 1. INSTRUCCION DINAMICA
# ---------------------------------------------------------
st.subheader("Instrucción de predicción")
st.info(
    f"Predecir **{config['horas_futuras']} horas** después del "
    f"**{config['referencia_texto'].lower()}**, utilizando un ciclo "
    f"histórico de **{config['ciclo_historico']} horas**."
)

c1, c2, c3 = st.columns(3)
c1.metric("Registro de referencia", config["referencia_texto"])
c2.metric("Horizonte", f"{config['horas_futuras']} horas")
c3.metric("Ciclo histórico", f"{config['ciclo_historico']} horas")

# ---------------------------------------------------------
# 2. TARJETAS DE RESULTADOS
# ---------------------------------------------------------
st.subheader("Resultados de la predicción")
tarjetas = st.columns(4)

for columna, (nombre, info) in zip(tarjetas, VARIABLES_UI.items()):
    dato = predicciones[info["clave"]]
    columna.metric(
        f"{info['icono']} {nombre}",
        f"{formato_numero(dato['valor'])} {info['unidad']}",
        help=f"Promedio de {dato['cantidad_registros']} registros históricos.",
    )

# ---------------------------------------------------------
# 3. HISTORICO: UNA VARIABLE POR VEZ
# ---------------------------------------------------------
st.divider()
st.subheader("Comportamiento histórico")

info = VARIABLES_UI[variable_nombre]
clave = info["clave"]
unidad = info["unidad"]

df_periodo = filtrar_periodo(df, periodo)
df_grafica = reducir_puntos(df_periodo)

fig_historico = px.line(
    df_grafica,
    x="hora",
    y=clave,
    labels={
        "hora": "Hora del registro",
        clave: f"{variable_nombre} ({unidad})",
    },
)
fig_historico.update_traces(line=dict(width=2))
fig_historico.update_layout(
    template="plotly_white",
    height=360,
    margin=dict(l=15, r=15, t=20, b=15),
    hovermode="x unified",
)
st.plotly_chart(fig_historico, use_container_width=True)

st.caption(
    f"Se muestran {len(df_grafica):,} puntos de {len(df_periodo):,} "
    "registros del período seleccionado.".replace(",", ".")
)

# ---------------------------------------------------------
# 4. BASE DE LA PREDICCION: DISTRIBUCION COMPACTA
# ---------------------------------------------------------
st.divider()
st.subheader("¿De dónde sale esta predicción?")
st.caption(
    "Distribución de todos los valores históricos que tiempo.py utilizó "
    "para calcular el promedio. Se resume en una sola caja para evitar "
    "una gráfica extensa con cientos de barras."
)

dato = predicciones[clave]
registros = dato["registros_utilizados"]
valores = [registro["valor"] for registro in registros]
promedio = dato["valor"]

if valores:
    fig_distribucion = go.Figure()

    fig_distribucion.add_trace(
        go.Box(
            y=valores,
            name=variable_nombre,
            boxpoints=False,
            boxmean=True,
            marker_color="#3B82A0",
            line_color="#3B82A0",
            fillcolor="rgba(59,130,160,0.22)",
            hovertemplate=f"Distribución de {variable_nombre}: %{{y:.2f}} {unidad}<extra></extra>",
        )
    )

    fig_distribucion.add_hline(
        y=promedio,
        line_dash="dash",
        line_color="#D97706",
        line_width=2,
        annotation_text=f"Promedio usado: {formato_numero(promedio)} {unidad}",
        annotation_position="top right",
    )

    fig_distribucion.update_layout(
        template="plotly_white",
        height=260,
        showlegend=False,
        margin=dict(l=15, r=15, t=35, b=15),
        yaxis_title=f"{variable_nombre} ({unidad})",
        xaxis_title="",
    )
    st.plotly_chart(fig_distribucion, use_container_width=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("Registros utilizados", len(valores))
    m2.metric("Promedio calculado", f"{formato_numero(promedio)} {unidad}")
    m3.metric("Hora objetivo", config["hora_objetivo"])

    with st.expander("Ver detalle de los registros utilizados"):
        tabla = pd.DataFrame(registros).rename(
            columns={"hora": "Hora histórica", "valor": f"Valor ({unidad})"}
        )
        st.dataframe(tabla, use_container_width=True, hide_index=True)
else:
    st.warning("No hay registros históricos disponibles para esta predicción.")

# ---------------------------------------------------------
# 5. RENDIMIENTO
# ---------------------------------------------------------
st.divider()
st.subheader("Rendimiento del procesamiento")

r1, r2, r3 = st.columns(3)
r1.metric(
    "Tiempo de ejecución",
    f"{formato_numero(resultado['tiempo_ejecucion_segundos'])} s",
)
r2.metric("Registros procesados", f"{config['total_registros']:,}".replace(",", "."))
r3.metric(
    "Hilos simultáneos permitidos",
    f"{config['max_hilos_simultaneos']} de {config['cantidad_hilos']}",
)
