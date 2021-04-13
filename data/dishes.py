import datetime
from sqlalchemy import orm
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Dish(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'dishes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    cooker = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("category.id"))
    categories = orm.relation("Category",
                              secondary="dish_to_category",
                              backref="dishes")
    user = orm.relation('User')
