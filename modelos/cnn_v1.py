import numpy as np
from PIL import Image
import tensorflow as tf
import os
from modelos.base_modelo import ModeloIA


class CNNv1(ModeloIA):
    def __init__(self, ruta_pesos, input_shape=(224, 224)):
        """
        Constructor del modelo CNNv1.

        :param ruta_pesos: Ruta al archivo .tflite con el modelo entrenado
        :param input_shape: Tamaño esperado por la CNN (alto, ancho)
        """
        self.__ruta = ruta_pesos
        self.__interpreter = None  # Intérprete TFLite
        self.__input_shape = input_shape

        # Detalles de entrada y salida del modelo TFLite
        self.__input_details = None
        self.__output_details = None

        # Diccionario de clases (ajustar según el entrenamiento)
        self.clases = {
            0: "Baja corriente",
            1: "Bloqueo por Gas",
            2: "Normal"
        }

    def cargar(self):
        """
        Carga el modelo TFLite desde la ruta especificada.
        Inicializa el intérprete y reserva memoria para los tensores.
        """
        if not os.path.exists(self.__ruta):
            raise FileNotFoundError(f"No se encontró el modelo en: {self.__ruta}")

        print(f"Cargando modelo TFLite desde {self.__ruta}...")

        # Crear intérprete TFLite
        self.__interpreter = tf.lite.Interpreter(model_path=self.__ruta)

        # Reservar memoria para los tensores
        self.__interpreter.allocate_tensors()

        # Obtener información de entrada y salida
        self.__input_details = self.__interpreter.get_input_details()
        self.__output_details = self.__interpreter.get_output_details()

        print("Modelo TFLite cargado exitosamente.")

    def preprocesar(self, ruta_imagen):
        """
        Toma la ruta de la imagen, la carga, la redimensiona y normaliza.

        Flujo de preprocesamiento:
        1. Cargar la imagen en RGB
        2. Redimensionar al tamaño esperado por la CNN
        3. Convertir a array NumPy
        4. Normalizar valores entre 0 y 1
        5. Expandir dimensiones para formar un batch de tamaño 1

        :param ruta_imagen: Ruta de la imagen a evaluar
        :return: Tensor listo para inferencia con TFLite
        """
        # 1. Cargar imagen y asegurar formato RGB
        img = Image.open(ruta_imagen).convert("RGB")

        # 2. Redimensionar al tamaño esperado por la CNN
        img = img.resize(self.__input_shape)

        # 3. Convertir a array NumPy (alto, ancho, canales)
        img_array = np.array(img, dtype=np.float32)

        # 4. Normalizar (0-255 → 0-1)
        img_array = img_array / 255.0

        # 5. Expandir dimensiones para crear el batch (1, alto, ancho, canales)
        img_tensor = np.expand_dims(img_array, axis=0)

        return img_tensor

    def predecir(self, entrada):
        """
        Realiza la inferencia sobre una imagen.

        Puede recibir:
        - La ruta de la imagen (str)
        - Un tensor ya preprocesado (np.ndarray)

        Flujo:
        1. Preprocesar la imagen (si es una ruta)
        2. Colocar el tensor en el input del intérprete
        3. Ejecutar inferencia con invoke()
        4. Leer tensor de salida
        5. Obtener clase predicha y confianza
        """
        if self.__interpreter is None:
            raise Exception("El modelo no ha sido cargado. Ejecuta .cargar() primero.")

        # Si entra un string, asumimos que es una ruta y preprocesamos
        if isinstance(entrada, str):
            X = self.preprocesar(entrada)
        else:
            X = entrada

        # Colocar tensor en el input del modelo
        self.__interpreter.set_tensor(self.__input_details[0]["index"], X)

        # Ejecutar inferencia
        self.__interpreter.invoke()

        # Obtener salida del modelo
        prediccion = self.__interpreter.get_tensor(self.__output_details[0]["index"])

        # Obtener clase con mayor probabilidad
        clase_idx = np.argmax(prediccion, axis=1)[0]
        confianza = np.max(prediccion)

        return {
            "clase": self.clases.get(clase_idx, "Desconocido"),
            "indice": int(clase_idx),
            "confianza": float(confianza),
            "raw_output": prediccion.tolist()
        }
