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