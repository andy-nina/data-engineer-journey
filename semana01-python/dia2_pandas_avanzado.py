import pandas as pd
import numpy as np

# ---- EXTRACT: cargamos datos de países y su info del COVID ----
url_covid = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
df_covid = pd.read_csv(url_covid)

print("=== Dataset original ===")
print(df_covid.head())
print(f"Filas: {df_covid.shape[0]}, Columnas: {df_covid.shape[1]}")

# ---- TRANSFORM 1: Manejo de nulos ----
print("\n=== Verificando nulos ===")
print(df_covid.isnull().sum())

df_covid = df_covid.fillna(0)

# ---- TRANSFORM 2: Tabla resumen por país (agregación múltiple) ----
resumen_paises = df_covid.groupby("Country").agg(
    total_confirmados=("Confirmed", "max"),
    total_muertes=("Deaths", "max"),
    total_recuperados=("Recovered", "max")
).reset_index()

resumen_paises["tasa_mortalidad_%"] = round(
    (resumen_paises["total_muertes"] / resumen_paises["total_confirmados"]) * 100, 2
)

print("\n=== Resumen por país (top 10 con más confirmados) ===")
top10 = resumen_paises.sort_values("total_confirmados", ascending=False).head(10)
print(top10)

# ---- TRANSFORM 3: Segundo DataFrame para practicar MERGE ----
continentes = pd.DataFrame({
    "Country": ["Peru", "Brazil", "US", "India", "Mexico", "Chile", "Colombia", "Ecuador"],
    "Continente": ["Sudamérica", "Sudamérica", "Norteamérica", "Asia", "Norteamérica", 
                   "Sudamérica", "Sudamérica", "Sudamérica"]
})

resumen_con_continente = pd.merge(
    resumen_paises, 
    continentes, 
    on="Country", 
    how="inner"
)

print("\n=== Resumen con continente (merge) ===")
print(resumen_con_continente)

# ---- LOAD: guardamos los resultados ----
resumen_paises.to_csv("resumen_paises_completo.csv", index=False)
resumen_con_continente.to_csv("resumen_con_continente.csv", index=False)

print("\n✅ Archivos guardados: resumen_paises_completo.csv y resumen_con_continente.csv")