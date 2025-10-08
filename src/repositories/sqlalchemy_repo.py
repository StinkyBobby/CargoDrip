from typing import List, TypeVar, Generic, Union, Optional

from sqlalchemy import update, delete, select, func


from src.config.db_data import db
from src.repositories import AbstractRepo


class SQLalchemy(AbstractRepo):
    model = None
    options = None


    async def create(self, data: dict):
        async with db.get_session() as session:
            model = self.model(**data) # создание обьекта модели
            session.add(model) # добавление обьекта в бд (мнимо)
            await session.commit() # Подтверждение добавления
            await session.refresh(model) # получение недостающих полей
            return model # возврат модели
        
    async def create_more(self, data: List[dict]):
        async with db.get_session() as session:
            modelList = []
            
            for row in data:
                model = self.model(**row)
                modelList.append(model)

            session.add_all(modelList)
            await session.commit()
            return modelList

    async def delete(self, **filters):
        async with db.get_session() as session:
            stmt = ( # общий запрос
                delete(self.model) # Удалить модель из базы данных  
                .filter_by(**filters) # Указание на массив строк
                .returning(self.model) # вернуть удаленные значения
            )
            result = await session.execute(stmt) # исполнить запрос
            await session.commit() # Сохранить изменения
            return result.scalar_one_or_none() # Вернуть модель
    
    async def update(self, data: dict, **filters):
        async with db.get_session() as session:
            stmt = ( # изменение значения
                update(self.model)
                .values(**data) # получение данных из словаря.
                .filter_by(**filters)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()
        
    async def find(self, **filters):
        async with db.get_session() as session:
            query = ( # получение значения 
                select(self.model)
                .filter_by(**filters)
            )

            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    async def find_all(self, limit: int = 100, offset: int = 0, order_by: str = None, **filters):
        async with db.get_session() as session:
            query = (
                select(self.model)
                .limit(limit)
                .offset(offset)
                .order_by(order_by)
                .filter_by(**filters)
            )
            result = await session.execute(query)
            return result.unique().scalars().all() 