import pandas as pd

class DataframeProcessor:
    def __init__(self, file):
        self.__file = file
        self.__df = None

    def cargar(self):
        """Carga el CSV"""
        self.__df = pd.read_csv(self.__file,encoding="cp1251",sep=";")
        #print(self.__df.columns.tolist())

        return self

    def limpiar_columnas(self):
        """Renombra y elimina columnas vacías"""
        self.__df = self.__df.rename(columns={
            "Дата/Время": "fecha_hora",
            "Событие": "evento"
        })

        self.__df = self.__df.dropna(axis=1, how="all")
        return self

    def convertir_fechas(self):
        """Convierte fecha/hora"""
        self.__df["fecha_hora"] = pd.to_datetime(
            self.__df["fecha_hora"],
            format="%d/%m/%Y %H:%M",
            errors="coerce"
        )

        self.__df["fecha"] = self.__df["fecha_hora"].dt.date
        self.__df["hora"] = self.__df["fecha_hora"].dt.hour
        return self

    def convertir_corriente(self): #convierte la columna a valores float
        """Convierte la columna de corriente a float"""
        self.__df["I motor act, A"] = (
            self.__df["I motor act, A"]
            .astype(str) #primero a texto
            .str.replace(",", ".", regex=False) #se cambia coma por punto
            .astype(float) #convertir a float
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
        return self.__df
