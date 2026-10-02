import pandas as pd
import requests
import sqlite3

def extraer_datos(url):
    try:
        response = requests.get(url, timeout=10)
        print(f"Status code: {response.status_code}")
        data = response.json()
        return data
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return None
resultado = extraer_datos("https://jsonplaceholder.typicode.com/users")
print(type(resultado))
print(f"Registros obtenidos: {len(resultado)}")

def transformar_datos(data):
    registros = []
    for usuario in data:
        registros.append({
            # completa tú las 3 claves: nombre, email, ciudad
            "nombre": usuario["name"],
            "correo": usuario["email"],
            "ciudad": usuario["address"]["city"]

        })
    df = pd.DataFrame(registros)
    return df

df = transformar_datos(resultado)
print(df) 

def cargar_datos(df, nombre_db, nombre_tabla):
    try:
        conexion = sqlite3.connect(nombre_db)
        df.to_sql(nombre_tabla, conexion, if_exists="replace", index=False)
        # aquí falta: guardar el DataFrame en la base de datos (pista: usa df.to_sql)
        # aquí falta: un print confirmando que se guardó bien
        print("\n✅ Datos cargados a la base de datos: usuarios.db")
        conexion.close()
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")

cargar_datos(df, "usuarios.db", "usuarios")