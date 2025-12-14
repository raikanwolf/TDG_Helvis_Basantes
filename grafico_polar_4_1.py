import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Cargar archivo
file_csv = "registro 5.csv"
df = pd.read_csv(file_csv, encoding="cp1251", sep=";")

# Renombrar columnas
df = df.rename(columns={
    "Дата/Время": "fecha/hora",
    "Событие": "evento"
})

# Eliminar columnas vacías
df = df.dropna(axis=1, how="all")

# Convertir fecha/hora a tipo datetime
df["fecha/hora"] = pd.to_datetime(df["fecha/hora"], errors="coerce")

# Limpiar y convertir corriente
df["I VSD total, A"] = df["I VSD total, A"].astype(str).str.replace(",", ".").astype(float)

# Crear columnas auxiliares
df["fecha"] = df["fecha/hora"].dt.date
df["hora"] = df["fecha/hora"].dt.hour
df["segundo"] = df["fecha/hora"].dt.second

# --- GRAFICO 1: Carta amperimétrica promedio por día ---
for fecha, grupo in df.groupby("fecha"):
    df_hourly = grupo.groupby("hora")["I VSD total, A"].mean().reset_index()

    valores = df_hourly["I VSD total, A"].values
    horas = df_hourly["hora"].values
    angulos = (horas / 24) * 2 * np.pi

    # Cerrar círculo
    angulos = np.append(angulos, angulos[0])
    valores = np.append(valores, valores[0])

    # Graficar
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angulos, valores, color="blue", linewidth=2.5)
    ax.set_title(f"Carta Amperimétrica - {fecha}", fontsize=14, pad=20)

    # Ajustes del gráfico
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim(0, max(valores) * 1.1)
    ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], fontsize=8)
    plt.show()

# --- GRAFICO 2: Representación segundo a segundo (línea temporal) ---
for fecha, grupo in df.groupby("fecha"):
    plt.figure(figsize=(12, 5))
    plt.plot(grupo["fecha/hora"], grupo["I VSD total, A"], color="green", linewidth=1)
    plt.title(f"Variación de corriente segundo a segundo - {fecha}", fontsize=14)
    plt.xlabel("Hora")
    plt.ylabel("Corriente (A)")
    plt.grid(True, alpha=0.3)
    plt.show()
