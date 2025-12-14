import os
import numpy as np
import matplotlib.pyplot as plt

class GraficoPolar:
    def __init__(self, df, carpeta_salida="graficos/por_dia"):
        self.df = df
        self.carpeta = carpeta_salida
        os.makedirs(self.carpeta, exist_ok=True)

    def generar_por_dia(self):
        dias = self.df["fecha"].unique()

        for dia in dias:
            self._graficar_dia(dia)

    def _graficar_dia(self, dia):
        df_dia = self.df[self.df["fecha"] == dia]
        df_hourly = (
            df_dia
            .groupby("hora")["I motor act, A"]
            .mean()
            .reset_index()
        )

        valores = df_hourly["I motor act, A"].values
        horas = df_hourly["hora"].values
        angulos = (horas / 24) * 2 * np.pi

        angulos = np.append(angulos, angulos[0])
        valores = np.append(valores, valores[0])

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, polar=True)

        ax.plot(angulos, valores, linewidth=2.5)

        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_ylim(0, max(valores) * 1.1)

        paso = 2
        maximo = np.ceil(max(valores))
        ticks = np.arange(0, maximo + paso, paso)
        ax.set_yticks(ticks)
        ax.set_yticklabels([f"{t:.0f}" for t in ticks], fontsize=8)

        ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
        ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], fontsize=8)

        plt.title(
            f"Carta Amperimétrica - Promedio por Hora ({dia})",
            fontsize=14,
            pad=20
        )

        filename = os.path.join(
            self.carpeta,
            f"carta_{dia}.png"
        )
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close(fig)
