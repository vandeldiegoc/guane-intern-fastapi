
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db.base_class import Base
from typing import TypeVar, Type, Generic
from pydantic import BaseModel
from db.sess import SessionLocal as session

modelType = TypeVar("modelType", bound=Base)
createSchemaType = TypeVar("createSchemaType", bound=BaseModel)
updateSchemaType = TypeVar("updateSchemaType", bound=BaseModel)


class crudRecipe(Generic[modelType, createSchemaType, updateSchemaType]):
    def __init__(self, model: Type[modelType]):
        self.model = model

    def create(self, db: session, obj_in: createSchemaType):
        db_obj = self.model(**obj_in)
        try:
            db.add(db_obj)
            db.commit()
            return(db_obj)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=405, 
                                detail='invali parameter or duplicate key value')

    def get(self, db: session, name: str):
        try:
            dog = db.query(self.model).filter(self.model.name == name).one()

        except NoResultFound:
            raise HTTPException(status_code=406,
                                detail="no record was found in the databases")
        return dog

    def get_all(self, db: session):
        dogs = db.query(self.model).all()
        return dogs

    def update(self, db: session, name: str, data: updateSchemaType):
        data = data.dict(exclude_unset=True)
        try:
            db.query(self.model).filter(self.model.name == name).\
            update(data)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=405, 
                                detail="error to try update dog for parameter")

    def delete(self, db: session, name: str):
        try:
            db.query(self.model).filter(self.model.name == name).\
            delete()
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=405,
                                detail="error to try delete dog")