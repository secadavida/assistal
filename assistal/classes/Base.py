import inspect
from typing import Any, Dict

class Base:
    def __init__(self, identificacion: int):
        self.identificacion = identificacion

    @classmethod
    def get_fields(cls) -> Dict[str, Any]:
        parameters = inspect.signature(cls.__init__).parameters
        fields = {}

        for name, param in parameters.items():
            if name != 'self':
                fields[name] = param.annotation if param.annotation is not inspect.Parameter.empty else Any

        return fields

    @classmethod
    def get_fields_listed(cls) -> list[str]:

        parameters = inspect.signature(cls.__init__).parameters

        return [param for param in parameters if param != 'self']
