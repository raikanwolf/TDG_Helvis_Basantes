from abc import ABC, abstractmethod

#creamos una interfaz y metodos abstractos para definir el que
#y despues el como
class ModeloIA(ABC):

    @abstractmethod
    def cargar(self):
        pass

    @abstractmethod
    def predecir(self, X):
        pass
