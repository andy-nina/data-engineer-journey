import pandas as pd

# EXTRACT: leemos un dataset público real (CSV de ejemplo)
url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
df = pd.read_csv(url)

print("Datos originales:")
print(df.head())
print(f"\nForma del dataset: {df.shape}")

# TRANSFORM: filtramos y agrupamos (algo típico en ETL)
peru = df[df["Country"] == "Peru"].copy()
peru["Date"] = pd.to_datetime(peru["Date"])

# Agregamos por mes
peru["Mes"] = peru["Date"].dt.to_period("M")
resumen_mensual = peru.groupby("Mes").agg({
    "Confirmed": "max",
    "Deaths": "max",
    "Recovered": "max"
}).reset_index()

print("\nResumen mensual Perú:")
print(resumen_mensual)

# LOAD: guardamos el resultado transformado
resumen_mensual.to_csv("resumen_mensual_peru.csv", index=False)
print("\n✅ Archivo guardado: resumen_mensual_peru.csv")