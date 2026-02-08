import pandas as pd
import re


class DataframeProcessor:
    def __init__(self, file):
        self.__file = file
        self.__df = None

    def cargar(self):
        """Carga el CSV"""
        self.__df = pd.read_csv(
            self.__file,
            encoding="cp1251",
            sep=";"
        )
        return self

    def limpiar_columnas(self):
        """Renombra y elimina columnas vacías"""
        self.__df = self.__df.rename(columns={
            "Дата/Время": "fecha_hora",
            "Событие": "evento"
        })

        self.__df = self.__df.dropna(axis=1, how="all")
        return self

    def normalizar_fecha_hora_texto(self):
        """
        Limpia el texto de fecha/hora para que pandas pueda interpretarlo.
        - Convierte AM/PM en español a inglés
        - Elimina espacios extra
        """

        self.__df["fecha_hora_raw"] = self.__df["fecha_hora"]

        self.__df["fecha_hora"] = (
            self.__df["fecha_hora"]
            .astype(str)
            .str.lower()
            .str.replace("a. m.", "am", regex=False)
            .str.replace("p. m.", "pm", regex=False)
            .str.replace("a.m.", "am", regex=False)
            .str.replace("p.m.", "pm", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        return self

    def convertir_fechas(self):
        """
        Convierte fecha_hora a datetime de forma robusta.
        Soporta múltiples formatos y convierte AM/PM a 24h automáticamente.
        """

        self.__df["fecha_hora"] = pd.to_datetime(
            self.__df["fecha_hora"],
            errors="coerce",
            dayfirst=True
        )

        # Auditoría
        n_invalidas = self.__df["fecha_hora"].isna().sum()
        total = len(self.__df)

        if n_invalidas > 0:
            print(
                f"[AVISO] {n_invalidas} de {total} filas "
                f"({n_invalidas / total:.2%}) "
                f"no pudieron convertirse a fecha válida."
            )

        # Extraer componentes normalizados
        self.__df["fecha"] = self.__df["fecha_hora"].dt.date
        self.__df["hora"] = self.__df["fecha_hora"].dt.hour

        return self

    def convertir_corriente(self):
        """Convierte la corriente a float"""
        self.__df["I motor act, A"] = (
            self.__df["I motor act, A"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )
        return self

    def procesar(self):
        """Pipeline completo"""
        return (
            self.cargar()
                .limpiar_columnas()
                .normalizar_fecha_hora_texto()
                .convertir_fechas()
                .convertir_corriente()
        )

    def get_df(self):
        return self.__df
