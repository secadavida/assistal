from datetime import datetime
from assistal.classes.Base import Base

class AssistanceEntry(Base):

    def __init__(self, identificacion: int, nombre_estudiante: str, estado: str, grado: int, grupo: str):
        super().__init__(identificacion)
        self.nombre_estudiante = nombre_estudiante
        self.estado = estado
        self.grado = grado
        self.grupo = grupo

