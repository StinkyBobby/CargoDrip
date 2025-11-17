from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    __abstract__ = True
    repr_cols_num = 10 
    repr_cols = tuple() 
    def __repr__(self):
        cols = []
        for attr in self.__mapper__.column_attrs:
            name = attr.key
            if name in self.repr_cols or len(cols) < self.repr_cols_num:
                cols.append(f"{name}={getattr(self, name)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
