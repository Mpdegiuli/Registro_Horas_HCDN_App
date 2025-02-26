import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Registro de Horas - HCDN", page_icon="📌", layout="wide")

# Estilo de colores para la app
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
    }
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #003366;
        text-align: center;
    }
    .stButton>button {
        background-color: #003366;
        color: white;
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #0055A4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Barra lateral con datos del desarrollador
st.sidebar.markdown("## 📌 Registro de Horas - HCDN")
st.sidebar.markdown("👩‍💻 **Desarrollado por:** Mariana de Giuli")
st.sidebar.markdown("📧 **Contacto:** [mpdegiuli@gmail.com](mailto:mpdegiuli@gmail.com)")

# Título de la aplicación
st.markdown('<p class="main-title">📊 Registro de Horas Trabajadas</p>', unsafe_allow_html=True)

# Sección de ingreso de datos
st.subheader("📅 Ingresá tus horas trabajadas")

# Variables
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
horas_trabajadas = {}

# Registro de horas por día
for dia in dias:
    st.write(f"### {dia}")
    falta = st.radio(f"¿Faltaste el {dia} con justificación?", ["No", "Sí"], key=f"falta_{dia}")

    if falta == "No":
        entrada = st.time_input(f"⏰ Hora de entrada ({dia})", key=f"entrada_{dia}")
        salida = st.time_input(f"🏁 Hora de salida ({dia})", key=f"salida_{dia}")
        pausa = st.number_input(f"⏸️ Minutos de pausa ({dia})", min_value=0, max_value=120, step=5, key=f"pausa_{dia}")

        # Cálculo de horas trabajadas
        horas_totales = (salida.hour * 60 + salida.minute) - (entrada.hour * 60 + entrada.minute) - pausa
        horas_trabajadas[dia] = max(0, horas_totales / 60)  # Convertimos a horas

    else:
        horas_trabajadas[dia] = 0  # Si faltó, 0 horas trabajadas

# Cálculo total
total_horas = sum(horas_trabajadas.values())
horas_requeridas = 35
horas_extra = total_horas - horas_requeridas

# Mostrar resultados
st.subheader("📊 Resumen de la Semana")
st.write(f"🔹 **Total acumulado:** {int(total_horas)} horas {int((total_horas % 1) * 60)} minutos")
st.write(f"🔹 **Horas faltantes para completar la semana:** {max(0, int(horas_requeridas - total_horas))} horas {int((horas_requeridas - total_horas) % 1 * 60)} minutos")
st.write(f"🔹 **Acumulado total de horas de más o de menos:** {int(horas_extra)} horas {int((horas_extra % 1) * 60)} minutos")

# Mensaje final
st.success("✅ Los datos fueron guardados correctamente.")
