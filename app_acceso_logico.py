import streamlit as st

st.title("🔐 Auditoría de Accesos Lógicos - ISO/IEC 27001")
st.markdown("#### Análisis simulado en entorno Linux")

# --- Opciones de simulación ---
st.sidebar.header("⚙️ Configuración de simulación")

simular_usuarios = st.sidebar.selectbox("Escenario de usuarios:", ["Normal", "Con cuentas compartidas"])
simular_intentos = st.sidebar.selectbox("Simular intentos fallidos:", ["No", "Sí"])
simular_mfa = st.sidebar.selectbox("Estado del MFA:", ["Configurado", "No configurado"])

# --- Datos según la simulación ---
if simular_usuarios == "Normal":
    usuarios = ["root", "daemon", "user1", "user2"]
    uids_duplicados = []
else:
    usuarios = ["root", "daemon", "user1", "user2"]
    uids_duplicados = ["1001"]

if simular_intentos == "Sí":
    intentos_fallidos = [
        "Jul 28 12:23:45 server sshd[12345]: Failed password for invalid user admin from 192.168.1.50 port 54712 ssh2"
    ]
else:
    intentos_fallidos = []

mfa_config = "AuthenticationMethods publickey,password" if simular_mfa == "Configurado" else ""

# --- Visualización ---
st.subheader("🧑‍💻 Usuarios del sistema:")
st.write(usuarios)

st.subheader("⚠️ UIDs duplicados (cuentas compartidas):")
if uids_duplicados:
    st.warning(f"Se detectaron: {', '.join(uids_duplicados)}")
else:
    st.success("No se detectaron UIDs duplicados.")

st.subheader("🚨 Intentos fallidos de acceso SSH:")
if intentos_fallidos:
    for intento in intentos_fallidos:
        st.code(intento)
else:
    st.info("No se detectaron intentos fallidos.")

st.subheader("🔐 MFA configurado:")
if mfa_config:
    st.success(f"MFA está configurado como: {mfa_config}")
else:
    st.error("MFA no está configurado.")
