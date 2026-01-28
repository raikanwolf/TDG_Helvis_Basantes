from tensorflow.keras.models import load_model
from modelos.base_modelo import ModeloIA

class CNNv1(ModeloIA): #heredamos de la interfaz

    def __init__(self, ruta_pesos):
        self.ruta = ruta_pesos #le damos la ruta de los pesos
        self.modelo = None

    def cargar(self): #carga pesos del modelo entrenado
        self.modelo = load_model(self.ruta)

    def predecir(self, X):
        return self.modelo.predict(X)
