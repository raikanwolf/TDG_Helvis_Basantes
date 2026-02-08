import os
import numpy as np
import matplotlib.pyplot as plt


class GraficoPolar:
    def __init__(self, df, carpeta_salida="graficos"):
        self.__df = df
        self.__carpeta = carpeta_salida
        os.makedirs(self.__carpeta, exist_ok=True)

    def generar_por_dia(self):
        dias = self.__df["fecha"].dropna().unique()

        for dia in dias:
            self._graficar_dia(dia)
        
        print(f"\n✔ Gráficos generados en la ruta:")
        print(f"📁 {os.path.abspath(self.__carpeta)}\n")

    def _graficar_dia(self, dia):
        df_dia = self.__df[self.__df["fecha"] == dia]

        df_hourly = (
            df_dia
            .groupby("hora")["I motor act, A"]
            .mean()
            .reset_index()
        )

        # Protección: día sin datos
        if df_hourly.empty:
            print(f"[AVISO] Día {dia} sin datos válidos.")
            return

        valores = df_hourly["I motor act, A"].values
        horas = df_hourly["hora"].values

        if len(valores) == 0:
            return

        angulos = (horas / 24) * 2 * np.pi

        # Cerrar la curva
        angulos = np.append(angulos, angulos[0])
        valores = np.append(valores, valores[0])

        # Crear figura limpia
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, polar=True)

        # Línea azul (único elemento visual)
        ax.plot(
            angulos,
            valores,
            color="blue",
            linewidth=2
        )

        # Configuración polar básica
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)

        # Quitar TODO el ruido visual
        ax.set_axis_off()

        # Ajustar límites radiales
        max_val = np.max(valores)
        ax.set_ylim(0, max_val * 1.05 if max_val > 0 else 1)

        # Guardar imagen
        filename = os.path.join(
            self.__carpeta,
            f"carta_{dia}.png"
        )

        plt.savefig(
            filename,
            dpi=224,
            bbox_inches="tight",
            pad_inches=0
        )
        plt.close(fig)
