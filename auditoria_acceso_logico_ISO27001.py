Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
# Código Python para análisis de acceso lógico en Linux
import os
import subprocess

# 1. Listar usuarios del sistema
def get_system_users():
    with open("/etc/passwd", "r") as f:
...         users = [line.split(":")[0] for line in f]
...     return users
... 
... # 2. Verificar UIDs duplicados (posibles cuentas compartidas)
... def get_duplicate_uids():
...     uids = subprocess.getoutput("cut -d: -f3 /etc/passwd | sort | uniq -d")
...     return uids.splitlines()
... 
... # 3. Buscar intentos fallidos de acceso SSH
... def check_ssh_failed_attempts():
...     result = subprocess.getoutput("journalctl -u ssh | grep 'Failed password'")
...     return result.splitlines()
... 
... # 4. Verificar si MFA está habilitado en SSH
... def check_mfa():
...     config = subprocess.getoutput("cat /etc/ssh/sshd_config | grep -i 'AuthenticationMethods'")
...     return config.strip()
... 
... # 5. Función principal de auditoría
... def main():
...     print("🧑‍💻 Usuarios del sistema:")
...     for user in get_system_users():
...         print(f" - {user}")
... 
...     print("\n⚠️ UIDs duplicados (cuentas compartidas):")
...     duplicates = get_duplicate_uids()
...     if duplicates:
...         print("\n".join(duplicates))
...     else:
...         print("No se encontraron.")
... 
...     print("\n🚨 Intentos fallidos de acceso SSH:")
...     failed_attempts = check_ssh_failed_attempts()
...     if failed_attempts:
...         for line in failed_attempts[:10]:  # Muestra solo los primeros 10
...             print(f" {line}")
...     else:
...         print("Sin intentos detectados.")
... 
...     print("\n🔐 MFA configurado:")
...     mfa = check_mfa()
    print(mfa if mfa else "No configurado")

if __name__ == "__main__":
    main()
