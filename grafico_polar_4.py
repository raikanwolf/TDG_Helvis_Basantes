import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# --- Cargar y limpiar datos ---
file_csv = "registro 3.csv"
df = pd.read_csv(file_csv, encoding="cp1251", sep=";")

# Renombrar columnas relevantes
df = df.rename(columns={
    "Дата/Время": "fecha/hora",
    "Событие": "evento"
})

# Eliminar columnas vacías
df = df.dropna(axis=1, how="all")

# Convertir columna de fecha y hora
df["fecha/hora"] = pd.to_datetime(df["fecha/hora"], errors="coerce")

# Reemplazar comas por puntos y convertir a float
df["I motor act, A"] = df["I motor act, A"].astype(str).str.replace(",", ".").astype(float)

# Crear columnas auxiliares
df["fecha"] = df["fecha/hora"].dt.date #2024-10-04
df["hora"] = df["fecha/hora"].dt.hour
df["segundo"] = df["fecha/hora"].dt.time

# --- Crear carpetas para guardar resultados ---
os.makedirs("graficos/por_dia", exist_ok=True)
os.makedirs("graficos/detalle", exist_ok=True)

# --- 1️⃣ GRAFICAR POR DÍA (promedio por hora) ---
#In the pandas library in Python, unique() is a function used to extract and return the unique values from a Series (a single column of a DataFrame).
dias = df["fecha"].unique()

for dia in dias:
    df_dia = df[df["fecha"] == dia]
    df_hourly = df_dia.groupby("hora")["I motor act, A"].mean().reset_index()

    valores = df_hourly["I motor act, A"].values
    horas = df_hourly["hora"].values
    angulos = (horas / 24) * 2 * np.pi

    # Cerrar el círculo
    angulos = np.append(angulos, angulos[0])
    valores = np.append(valores, valores[0])

    # Crear figura
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angulos, valores, color="blue", linewidth=2.5)

    # --- 📊 Personalizar la escala radial ---
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim(0, max(valores) * 1.1)

    # 🔧 Escala del eje radial: cambia 2 → 5 si quieres saltos mayores
    paso = 2
    maximo = np.ceil(max(valores))
    ticks = np.arange(0, maximo + paso, paso)
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"{t:.0f}" for t in ticks], fontsize=8)

    # Etiquetas de las horas
    ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], fontsize=8)

    plt.title(f"Carta Amperimétrica - Promedio por Hora ({dia})", fontsize=14, pad=20)

    # Guardar imagen
    filename = f"graficos/por_dia/carta_{dia}.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


"""
# --- 2️⃣ GRAFICAR DETALLE SEGUNDO A SEGUNDO ---
for dia in dias:
    df_detalle = df[df["fecha"] == dia]

    plt.figure(figsize=(12, 6))
    plt.plot(df_detalle["fecha/hora"], df_detalle["I motor act, A"], color="orange", linewidth=1)
    plt.title(f"Variación de Corriente Segundo a Segundo ({dia})", fontsize=14)
    plt.xlabel("Hora")
    plt.ylabel("Corriente (A)")
    plt.grid(True)
    plt.tight_layout()

    # Guardar imagen
    filename = f"graficos/detalle/detalle_{dia}.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
"""