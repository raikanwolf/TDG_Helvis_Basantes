from abc import ABC, abstractmethod

class ModeloIA(ABC):
    @abstractmethod
    def cargar(self):
        """Carga los pesos del modelo en memoria."""
        pass

    @abstractmethod
    def preprocesar(self, entrada_cruda):
        """Transforma la entrada (ruta imagen, df, array) al formato del tensor."""
        pass

    @abstractmethod
    def predecir(self, entrada_procesada):
        """Realiza la inferencia."""
        pass