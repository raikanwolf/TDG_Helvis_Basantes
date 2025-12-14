import pandas as pd

class Dataframe:
    def __init__(self, file):
        self.file = file
        self.df = None

    def cargar(self):
        """Carga el CSV"""
        self.df = pd.read_csv(self.file,encoding="cp1251",sep=";")
        #print(self.df.columns.tolist())

        return self

    def limpiar_columnas(self):
        """Renombra y elimina columnas vacías"""
        self.df = self.df.rename(columns={
            "Дата/Время": "fecha_hora",
            "Событие": "evento"
        })

        self.df = self.df.dropna(axis=1, how="all")
        return self

    def convertir_fechas(self):
        """Convierte fecha/hora"""
        self.df["fecha_hora"] = pd.to_datetime(
            self.df["fecha_hora"],
            errors="coerce"
        )

        self.df["fecha"] = self.df["fecha_hora"].dt.date
        self.df["hora"] = self.df["fecha_hora"].dt.hour
        return self

    def convertir_corriente(self):
        """Convierte la columna de corriente a float"""
        self.df["I motor act, A"] = (
            self.df["I motor act, A"]
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
                .convertir_fechas()
                .convertir_corriente()
        )

    def get_df(self):
        return self.df
