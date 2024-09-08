import inspect
from typing import Any, Dict, List

class Base:

    none_handlers = {}

    def __init__(self, identificacion: int):
        self.identificacion = identificacion

    @classmethod
    def get_fields(cls, *drop) -> Dict[str, Any]:
        parameters = inspect.signature(cls.__init__).parameters
        fields = {}

        for name, param in parameters.items():
            if name in drop:
                fields[name] = None
            elif name != 'self':
                fields[name] = param.annotation if param.annotation is not inspect.Parameter.empty else Any

        return fields

    @classmethod
    def get_fields_listed(cls) -> List[str]:

        parameters = inspect.signature(cls.__init__).parameters

        return [param for param in parameters if param != 'self']

    @classmethod
    def from_list(cls, values: list, allow_nones: bool = False) -> dict:
        parameters = inspect.signature(cls.__init__).parameters
        
        # remove 'self' from parameters
        attributes = [param for param in parameters if param != 'self']
        
        # Ensure that the number of values matches the number of attributes
        if len(attributes) != len(values):
            raise ValueError(f"Expected {len(attributes)} values, got {len(values)}.")
        
        # create a dictionary by pairing attributes with corresponding values
        record_dict = dict(zip(attributes, values))

        # add items that are either not None, or are None but have a handler registered
        if not allow_nones:

            filtered_dict = {}

            for k, v in record_dict.items():
                if v is not None:
                    filtered_dict[k] = v
                else:
                    if k in cls.none_handlers:
                        filtered_dict[k] = cls.none_handlers[k]()

            return filtered_dict
        else:
            return record_dict
