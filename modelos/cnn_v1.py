from tensorflow.keras.models import load_model
from modelos.base_modelo import ModeloIA

class CNNv1(ModeloIA): #heredamos de la interfaz

    def __init__(self, ruta_pesos):
        self.__ruta = ruta_pesos #le damos la ruta de los pesos
        self.__modelo = None

    def cargar(self): #carga pesos del modelo entrenado
        self.__modelo = load_model(self.__ruta)

    def predecir(self, X):
        return self.__modelo.predict(X)
