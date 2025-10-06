from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    __abstract__ = True # не будет отображаться как таблица в базе данных
    # настройки для __repr__
    repr_cols_num = 10 
    repr_cols = tuple() # кортеж с именами колонок
    # вывод в таблицу по примеру: <User id=1, name=Name, email=email@gmail.com>
    def __repr__(self):
        cols = []
        for attr in self.__mapper__.column_attrs:
            name = attr.key
            if name in self.repr_cols or len(cols) < self.repr_cols_num:
                cols.append(f"{name}={getattr(self, name)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
