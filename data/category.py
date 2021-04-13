import sqlalchemy
from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'dish_to_category',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('dishes', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('dishes.id')),
    sqlalchemy.Column('category', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('category.id'))
)


class Category(SqlAlchemyBase):
    __tablename__ = 'category'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)