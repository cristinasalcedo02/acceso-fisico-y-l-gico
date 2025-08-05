import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO, BytesIO
from datetime import datetime
from fpdf import FPDF
import hashlib

st.set_page_config(page_title="Auditoría de Acceso Lógico - ISO/IEC 27001", layout="wide")

st.title("🔐 Auditoría de Accesos Lógicos - ISO/IEC 27001")
st.markdown("""
Esta aplicación permite analizar el control de accesos lógicos en sistemas Linux simulando una auditoría basada en la Cláusula A.9 de la norma ISO/IEC 27001. 
Puedes subir archivos reales del sistema como `passwd`, `sshd_config` y logs SSH para detectar cuentas compartidas, accesos fallidos y configuración de MFA. 
Incluye gráficas interactivas, edición de usuarios, simulación de hashes y un sistema de puntuación de riesgo.
""")

# 1. Carga de archivos
st.sidebar.header("⚙️ Subir archivos reales")
passwd_file = st.sidebar.file_uploader("Archivo passwd", type=["txt"])
sshd_file = st.sidebar.file_uploader("Archivo sshd_config", type=["txt"])
log_file = st.sidebar.file_uploader("Log de SSH", type=["txt"])

usuarios = []
uids = []
hashes = []
puntaje = 0

if passwd_file:
    content = passwd_file.read().decode("utf-8")
    lines = content.strip().split('\n')
    for line in lines:
        parts = line.split(":")
        if len(parts) > 2:
            usuario = parts[0]
            uid = parts[2]
            hash_uid = hashlib.sha256((usuario + uid).encode()).hexdigest()
            usuarios.append(usuario)
            uids.append(uid)
            hashes.append(hash_uid[:12] + "...")

    df_usuarios = pd.DataFrame({"Usuario": usuarios, "UID": uids, "Hash Simulado": hashes})
    st.subheader("👨‍💻 Usuarios del sistema")
    st.data_editor(df_usuarios, use_container_width=True)

    # UIDs duplicados
    duplicados = df_usuarios[df_usuarios.duplicated('UID', keep=False)]
    st.subheader("⚠️ UIDs duplicados (posibles cuentas compartidas)")
    if not duplicados.empty:
        st.warning("Se detectaron posibles cuentas compartidas:")
        st.dataframe(duplicados)
        puntaje += 1
    else:
        st.success("No se detectaron UIDs duplicados.")

# 2. Log de accesos fallidos
if log_file:
    content = log_file.read().decode("utf-8")
    lines = content.strip().split('\n')
    fechas = []
    for line in lines:
        try:
            partes = line.split()
            fecha = "{} {}".format(partes[0], partes[1])
            fecha_dt = datetime.strptime(fecha, "%b %d")
            fechas.append(fecha_dt.strftime("%m-%d"))
        except:
            continue
    if fechas:
        df_fechas = pd.DataFrame({"Fecha": fechas})
        fig = px.histogram(df_fechas, x="Fecha", title="🚨 Intentos fallidos de acceso por día")
        st.plotly_chart(fig, use_container_width=True)
        puntaje += 1

# 3. Verificación de MFA
if sshd_file:
    config = sshd_file.read().decode("utf-8")
    st.subheader("🔐 MFA configurado")
    if "AuthenticationMethods" in config:
        metodo = [l for l in config.splitlines() if "AuthenticationMethods" in l][0]
        st.success(f"MFA está configurado como: {metodo}")
        puntaje += 1
    else:
        st.error("MFA no está configurado.")

# 4. Puntuación de Riesgo
st.subheader("📊 Evaluación del Riesgo")
riesgo = "Alto" if puntaje <= 1 else ("Medio" if puntaje == 2 else "Bajo")
st.info(f"Nivel de riesgo detectado: **{riesgo}** ({puntaje}/3 controles cumplidos)")

# 5. Exportar PDF
st.subheader("📄 Exportar Reporte en PDF")
if st.button("Generar Reporte PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Auditoría de Accesos Lógicos", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Usuarios cargados: {len(usuarios)}\nRiesgo Evaluado: {riesgo}\nMFA Configurado: {'Sí' if puntaje >= 3 else 'No'}")
    pdf.ln(5)
    pdf.cell(200, 10, txt="Fin del informe.", ln=True)
    buffer = BytesIO()
    pdf.output(buffer)
    st.download_button("Descargar PDF", data=buffer.getvalue(), file_name="informe_auditoria.pdf", mime="application/pdf")
