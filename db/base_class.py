from typing import Dict, Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import inspect

class_registry: Dict = {}

# mapping object tables to use from conection session 
@as_declarative(class_registry= class_registry)
class Base:
    id: Any
    __name__: str


    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def _asdict(self) -> Dict[str, Any]:
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }

