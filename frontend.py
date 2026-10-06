import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Dirección del backend. En la computadora es la local;
# cuando esté publicado se cambia con la variable de entorno API_URL.
API = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Detección de Punteo Electoral", layout="wide")

# session_state es la "memoria" de Streamlit: guarda el token entre pantallas
if "token" not in st.session_state:
    st.session_state.token = None


def encabezados():
    return {"Authorization": f"Bearer {st.session_state.token}"}


def pantalla_login():
    st.title("Detección de Punteo Electoral")
    st.subheader("Iniciar sesión")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        r = requests.post(f"{API}/login", data={"username": usuario, "password": clave})
        if r.status_code == 200:
            st.session_state.token = r.json()["access_token"]
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")


def pantalla_dashboard():
    st.title("Dashboard de mesas")

    r = requests.get(f"{API}/resumen", headers=encabezados())
    if r.status_code == 401:
        st.session_state.token = None
        st.rerun()
    datos = r.json()

    df = pd.DataFrame(datos)
    df["situacion"] = df["estado"].apply(lambda e: "OK" if e == "OK" else "Alerta")

    # Tarjetas con los números principales
    c1, c2, c3 = st.columns(3)
    c1.metric("Mesas cargadas", len(df))
    c2.metric("Mesas con alerta", int((df["situacion"] == "Alerta").sum()))
    c3.metric("Participación promedio", f"{df['participacion'].mean():.1f}%")

    # Tabla
    st.subheader("Detalle por mesa")
    tabla = df[["nombre", "electores", "total_votos", "participacion", "estado"]]
    tabla.columns = ["Mesa", "Electores", "Votos", "Participación (%)", "Estado"]
    st.dataframe(tabla, hide_index=True)

    # Gráfico 1: votos por agrupación en cada mesa
    st.subheader("Votos por agrupación")
    filas = [
        {"Mesa": d["nombre"], "Agrupación": a, "Votos": c}
        for d in datos
        for a, c in d["votos"].items()
    ]
    fig1 = px.bar(pd.DataFrame(filas), x="Mesa", y="Votos", color="Agrupación", barmode="stack")
    st.plotly_chart(fig1)

    # Gráfico 2: participación, con línea en el 100%
    st.subheader("Participación por mesa")
    fig2 = px.bar(
        df, x="nombre", y="participacion", color="situacion",
        color_discrete_map={"OK": "#2E7D32", "Alerta": "#C62828"},
        labels={"nombre": "Mesa", "participacion": "Participación (%)", "situacion": "Situación"},
    )
    fig2.add_hline(y=100, line_dash="dash", annotation_text="100% de los electores")
    st.plotly_chart(fig2)


def pantalla_cargar():
    st.title("Cargar mesa")

    with st.form("form_mesa"):
        nombre = st.text_input("Nombre de la mesa (ej: Mesa 30)")
        electores = st.number_input("Electores habilitados", min_value=1, step=1)
        st.write("Votos por agrupación")
        v1 = st.number_input("Alternativa Académica", min_value=0, step=1)
        v2 = st.number_input("La 15", min_value=0, step=1)
        v3 = st.number_input("La Ues", min_value=0, step=1)
        enviado = st.form_submit_button("Guardar mesa")

    if enviado:
        cuerpo = {
            "nombre": nombre,
            "electores": int(electores),
            "votos": [
                {"agrupacion": "Alternativa Académica", "cantidad": int(v1)},
                {"agrupacion": "La 15", "cantidad": int(v2)},
                {"agrupacion": "La Ues", "cantidad": int(v3)},
            ],
        }
        r = requests.post(f"{API}/mesas", json=cuerpo, headers=encabezados())

        if r.status_code == 201:
            estado = r.json()["estado"]
            if estado == "OK":
                st.success(f"Mesa guardada. Resultado del detector: {estado}")
            else:
                st.warning(f"Mesa guardada. Resultado del detector: {estado}")
        elif r.status_code == 409:
            st.error("Ya existe una mesa con ese nombre. Usá otro nombre.")
        elif r.status_code == 422:
            st.error("Datos inválidos: revisá que haya un nombre y al menos un voto cargado.")
        else:
            st.error(f"Error inesperado ({r.status_code})")


def pantalla_predicciones():
    st.title("Predicciones de riesgo")
    st.write(
        "El modelo de Machine Learning (Random Forest) mira la participación y la "
        "concentración de votos de cada mesa y predice si el riesgo es ALTO o BAJO. "
        "Al lado se muestra lo que dicen las reglas fijas del detector."
    )

    r = requests.get(f"{API}/resumen", headers=encabezados())
    if r.status_code == 401:
        st.session_state.token = None
        st.rerun()

    filas = []
    for d in r.json():
        if d["total_votos"] == 0:
            continue  # sin votos no se puede predecir
        rp = requests.get(f"{API}/prediccion/{d['id']}", headers=encabezados())
        riesgo = rp.json().get("riesgo_predicho", "?")
        concentracion = max(d["votos"].values()) / d["total_votos"] * 100
        filas.append({
            "Mesa": d["nombre"],
            "Participación (%)": d["participacion"],
            "Concentración máxima (%)": round(concentracion, 1),
            "Regla del detector": d["estado"],
            "Riesgo según el modelo": riesgo,
        })

    df = pd.DataFrame(filas)

    c1, c2 = st.columns(2)
    c1.metric("Mesas analizadas", len(df))
    c2.metric("Mesas con riesgo ALTO", int((df["Riesgo según el modelo"] == "ALTO").sum()))

    st.subheader("Resultado por mesa")
    st.dataframe(df, hide_index=True)

    st.subheader("Mapa de riesgo")
    fig = px.scatter(
        df, x="Participación (%)", y="Concentración máxima (%)",
        color="Riesgo según el modelo", hover_name="Mesa",
        color_discrete_map={"ALTO": "#C62828", "BAJO": "#2E7D32"},
    )
    fig.add_vline(x=100, line_dash="dash", annotation_text="100% de participación")
    fig.add_hline(y=70, line_dash="dash", annotation_text="70% de concentración")
    st.plotly_chart(fig)


# ---- Programa principal ----
if st.session_state.token is None:
    pantalla_login()
else:
    st.sidebar.title("Menú")
    pagina = st.sidebar.radio("Pantalla", ["Dashboard", "Cargar Zona", "Predicciones"])
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.token = None
        st.rerun()

    if pagina == "Dashboard":
        pantalla_dashboard()
    elif pagina == "Cargar Zona":
        pantalla_cargar()
    elif pagina == "Predicciones":
        pantalla_predicciones()