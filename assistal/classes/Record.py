"""A Record, as represented internally and in the documents"""

from datetime import datetime
from assistal.classes.Base import Base

class Record(Base):

    @staticmethod
    def _handler_timestamp():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    none_handlers = {
        "timestamp": _handler_timestamp
    }

    def __init__(self, estado: str, timestamp: str, acudiente: str, parentesco: str, grado: int, grupo: str, identificacion: int, nombre_estudiante: str):
        super().__init__(identificacion)
        self.estado = estado
        self.timestamp = timestamp
        self.acudiente = acudiente
        self.parentesco = parentesco
        self.grado = grado
        self.grupo = grupo
        self.nombre_estudiante = nombre_estudiante

