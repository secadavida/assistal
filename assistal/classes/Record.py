"""A Record, as represented internally and in the documents"""

from assistal.classes.Base import Base

class Record(Base):
    def __init__(self, acudiente: str, parentesco: str, grado: int, grupo: str, identificacion: int, nombre_estudiante: str):
        super().__init__(identificacion)
        self.acudiente = acudiente
        self.parentesco = parentesco
        self.grado = grado
        self.grupo = grupo
        self.nombre_estudiante = nombre_estudiante
