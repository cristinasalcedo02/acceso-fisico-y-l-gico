import streamlit as st

# Datos simulados
usuarios = ["root", "daemon", "user1", "user2"]
uids_duplicados = ["1001"]
intentos_fallidos = [
    "Jul 28 12:23:45 server sshd[12345]: Failed password for invalid user admin from 192.168.1.50 port 54712 ssh2"
]
mfa_config = "AuthenticationMethods publickey,password"

st.title("🔐 Auditoría de Accesos Lógicos - ISO/IEC 27001")
st.markdown("#### Análisis simulado en entorno Linux")

st.subheader("🧑‍💻 Usuarios del sistema:")
st.write(usuarios)

st.subheader("⚠️ UIDs duplicados (cuentas compartidas):")
if uids_duplicados:
    st.warning(f"Se detectaron: {', '.join(uids_duplicados)}")
else:
    st.success("No se detectaron UIDs duplicados.")

st.subheader("🚨 Intentos fallidos de acceso SSH:")
for intento in intentos_fallidos:
    st.code(intento)

st.subheader("🔐 MFA configurado:")
if mfa_config:
    st.success(f"MFA está configurado como: {mfa_config}")
else:
    st.error("MFA no está configurado.")
