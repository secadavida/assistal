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

    @classmethod
    def from_list(cls, values: list) -> dict:
        parameters = inspect.signature(cls.__init__).parameters
        
        # remove 'self' from parameters
        attributes = [param for param in parameters if param != 'self']
        
        # Ensure that the number of values matches the number of attributes
        if len(attributes) != len(values):
            raise ValueError(f"Expected {len(attributes)} values, got {len(values)}.")
        
        # create a dictionary by pairing attributes with corresponding values
        record_dict = dict(zip(attributes, values))
        
        # remove keys with None values
        record_dict = {k: v for k, v in record_dict.items() if v is not None}
        
        return record_dict
