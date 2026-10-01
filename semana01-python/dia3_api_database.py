import pandas as pd
import requests
import sqlite3

# ---- EXTRACT ----
url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url, timeout=10)

print(f"Status code: {response.status_code}")

data = response.json()
print(f"Usuarios recibidos: {len(data)}")

# ---- TRANSFORM ----
registros = []
for usuario in data:
    registros.append({
        "nombre": usuario["name"],
        "email": usuario["email"],
        "ciudad": usuario["address"]["city"]
    })

df = pd.DataFrame(registros)

print("\n=== Datos transformados ===")
print(df)

# ---- LOAD: guardamos en base de datos SQLite ----
conexion = sqlite3.connect("usuarios.db")
df.to_sql("usuarios", conexion, if_exists="replace", index=False)

print("\n✅ Datos cargados a la base de datos: usuarios.db")

# ---- Verificación: leemos de vuelta con una consulta SQL ----
query = "SELECT * FROM usuarios WHERE ciudad LIKE '%burgh%'"
resultado = pd.read_sql(query, conexion)

print("\n=== Verificación: consulta SQL ===")
print(resultado)

conexion.close()