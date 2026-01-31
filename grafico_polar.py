import os
import numpy as np
import matplotlib.pyplot as plt


class GraficoPolar:
    def __init__(self, df, carpeta_salida="graficos/por_dia"):
        self.__df = df
        self.__carpeta = carpeta_salida
        os.makedirs(self.__carpeta, exist_ok=True)

    def generar_por_dia(self):
        dias = self.__df["fecha"].dropna().unique()

        for dia in dias:
            self._graficar_dia(dia)

    def _graficar_dia(self, dia):
        """Método protegido: uso interno de la clase"""
        df_dia = self.__df[self.__df["fecha"] == dia]

        df_hourly = (
            df_dia
            .groupby("hora")["I motor act, A"]
            .mean()
            .reset_index()
        )

        # 🚨 Protección: no hay datos válidos
        if df_hourly.empty:
            print(f"[AVISO] No hay datos válidos para el día {dia}. Se omite el gráfico.")
            return

        valores = df_hourly["I motor act, A"].values
        horas = df_hourly["hora"].values

        if len(valores) == 0:
            return

        angulos = (horas / 24) * 2 * np.pi

        # Cerrar el gráfico polar
        angulos = np.append(angulos, angulos[0])
        valores = np.append(valores, valores[0])

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, polar=True)

        ax.plot(angulos, valores, linewidth=2.5)

        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)

        # ⚠️ Protección contra valores constantes (ej: todos 0)
        max_val = max(valores)
        if max_val == 0:
            ax.set_ylim(0, 1)
        else:
            ax.set_ylim(0, max_val * 1.1)

        # Escala radial
        paso = 5
        maximo = np.ceil(max_val if max_val > 0 else 1)
        ticks = np.arange(0, maximo + paso, paso)
        ax.set_yticks(ticks)
        ax.set_yticklabels([f"{t:.0f}" for t in ticks], fontsize=8)

        # Etiquetas horarias
        ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
        ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], fontsize=8)

        plt.title(
            f"Carta Amperimétrica - Promedio por Hora ({dia})",
            fontsize=14,
            pad=20
        )

        filename = os.path.join(
            self.__carpeta,
            f"carta_{dia}.png"
        )
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close(fig)
