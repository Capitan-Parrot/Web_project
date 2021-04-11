import flask
from flask import jsonify, request
from . import db_session
from .dishes import Dish

blueprint = flask.Blueprint(
    'dishes_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/dishes')
def get_dishes():
    db_sess = db_session.create_session()
    dishes = db_sess.query(Dish).all()
    return flask.jsonify(
        {
            'dishes':
                [item.to_dict(only=('id', 'cooker', 'title', 'category', 'work_size'))
                 for item in dishes]
        }
    )


@blueprint.route('/api/dishes/<int:dish_id>', methods=['GET'])
def get_one_dish(dish_id):
    db_sess = db_session.create_session()
    dish = db_sess.query(Dish).get(dish_id)
    if not dish:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'dishes': dish.to_dict(only=('id', 'cooker', 'title', 'category', 'work_size'))
        }
    )


@blueprint.route('/api/dishes', methods=['POST'])
def create_dish():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['cooker', 'title', 'category', 'work_size']):
        return jsonify({'error': 'Bad request'})
    elif 'id' in request.json and db_sess.execute(f'SELECT * FROM dishes WHERE (id = {request.json["id"]})').fetchone():
        return jsonify({'error': 'Id already exists'})
    dish = Dish(
        cooker=request.json['cooker'],
        title=request.json['title'],
        work_size=request.json['work_size'],
        category=request.json.get['category']
    )
    db_sess.add(dish)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/dishes/<int:dish_id>', methods=['DELETE'])
def delete_job(dish_id):
    db_sess = db_session.create_session()
    dish = db_sess.query(Dish).get(dish_id)
    if not dish:
        return jsonify({'error': 'Not found'})
    db_sess.delete(dish)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/dishes/<int:dish_id>', methods=['POST'])
def edit_dishes(dish_id):
    db_sess = db_session.create_session()
    old_dish = db_sess.query(Dish).get(dish_id)
    if not old_dish:
        return jsonify({'error': 'Empty request'})
    db_sess.delete(old_dish)
    dish = Dish(
        id=request.json.get('id', old_dish.id),
        cooker=request.json.get('cooker', old_dish.team_leader),
        title=request.json.get('title', old_dish.title),
        work_size=request.json.get('work_size', old_dish.work_size),
        category=request.json.get('category', old_dish.category)
    )
    db_sess.add(dish)
    db_sess.commit()
    return jsonify({'success': 'OK'})