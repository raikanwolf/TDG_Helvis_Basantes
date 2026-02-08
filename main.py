import os
import tkinter as tk
from tkinter import filedialog
from dataframeProcessor import DataframeProcessor
from grafico_polar import GraficoPolar


def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # ← ventana al frente

    file = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(
            ("Archivos CSV", "*.csv"),
            ("Archivos de texto", "*.txt"),
            ("Todos", "*.*")
        )
    )
    root.destroy() #Destruye completamente la ventana raíz y libera recursos
    return file


def menu(op):
    if op == 1:
        file = seleccionar_archivo()
        if not file:
            print("Archivo no seleccionado")
            return

        df = DataframeProcessor(file).procesar().get_df() #esto sirve para obtener el csv y limpia las columnas luego **

        print("Generando gráficos polares...")
        GraficoPolar(df).generar_por_dia() # ** pasamos ese dataframe a grafico plar

        print("Gráficos generados correctamente")
    
    elif op == 3:
        file = seleccionar_archivo()
        if not file:
            print("Archivo no seleccionado")
            return

        df = DataframeProcessor(file).procesar().get_df()

        print("\n📊 PREVISUALIZACIÓN DEL DATAFRAME")
        print("-" * 40)

        print("\nColumnas:")
        print(df.columns.tolist())

        print("\nTipos de datos:")
        print(df.dtypes)

        print("\nPrimeras 5 filas:")
        print(df.head())

        print("\nÚltimas 5 filas:")
        print(df.tail())

        print("\nInformación general:")
        df.info()

        print("\nEstadísticas descriptivas:")
        print(df.describe(include="all"))
        
        
        print("\n🧪 CONTROL DE CALIDAD DE DATOS")
        print("-" * 40)

        # ---- FECHA / HORA ----
        if "fecha_hora" in df.columns:
            total_filas = len(df)
            fechas_invalidas = df["fecha_hora"].isna().sum()
            fechas_validas = total_filas - fechas_invalidas

            print("\n📅 Columna: fecha_hora")
            print(f"Total de filas        : {total_filas}")
            print(f"Fechas válidas        : {fechas_validas}")
            print(f"Fechas inválidas (NaT): {fechas_invalidas}")
        else:
            print("\n⚠️ La columna 'fecha_hora' no existe en el DataFrame")

        # ---- CORRIENTE DEL MOTOR ----
        columna_corriente = "I motor act, A"

        if columna_corriente in df.columns:
            corriente = df[columna_corriente]

            total = len(corriente)
            nan_corriente = corriente.isna().sum()
            validas = total - nan_corriente
            no_positivas = (corriente <= 0).sum()

            print("\n⚡ Columna: I motor act, A")
            print(f"Total de filas          : {total}")
            print(f"Valores válidos         : {validas}")
            print(f"Valores NaN             : {nan_corriente}")
            print(f"Valores <= 0 (inválidos): {no_positivas}")
        else:
            print("\n⚠️ La columna 'I motor act, A' no existe en el DataFrame")



if __name__ == '__main__':
    '''menu de opciones'''
    op=0
   
    while(op!=4):

        print("\t.:IA electrosumergible:.")
        print("acciones disponibles")
        print("1-Cargar datos") #listo
        print("2-Entrenar modelo")
        print("3-")
        print("4-salir")

        op=int(input("ingrese el numero de opcion: "))
        print("\n")
        if (op!=4):
            menu(op)