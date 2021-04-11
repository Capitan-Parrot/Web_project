from flask_restful import reqparse, abort, Api, Resource
from flask import session, jsonify
from data.dishes import Dish
from data.parser_dish import parser
# noinspection PyUnresolvedReferences
from data import db_session


def abort_if_users_not_found(dish_id):
    session = db_session.create_session()
    dish = session.query(Dish).get(dish_id)
    if not dish:
        abort(404, message=f"dish {dish_id} not found")


class DishesResource(Resource):
    def get(self, dish_id):
        abort_if_users_not_found(dish_id)
        session = db_session.create_session()
        dish = session.query(Dish).get(dish_id)
        return jsonify({'dish': dish.to_dict(
            only=('id', 'cooker', 'title', 'category', 'work_size'))})

    def delete(self, dish_id):
        abort_if_users_not_found(dish_id)
        session = db_session.create_session()
        dish = session.query(Dish).get(dish_id)
        session.delete(dish)
        session.commit()
        return jsonify({'success': 'OK'})


class DishesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        dishes = session.query(dish).all()
        return jsonify({'dishes': [item.to_dict(
            only=('id', 'cooker', 'title', 'category', 'work_size'))
            for item in dishes]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        dish = Dish(
            cooker=args['cooker'],
            title=args['title'],
            work_size=args['work_size'],
            category=args['category']
        )
        session.add(dish)
        session.commit()
        return jsonify({'success': 'OK'})


