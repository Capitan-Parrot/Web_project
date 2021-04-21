from flask import Flask, render_template, redirect, make_response, jsonify, request, url_for
from data import db_session
from data.users import User
from data.dishes import Dish
from data.category import Category
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.add_dish import DishesForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import reqparse, abort, Api, Resource
import users_resource
import dishes_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'incredible_secret_key'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с такой почтой уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add_dish',  methods=['GET', 'POST'])
@login_required
def add_dish():
    form = DishesForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dish = Dish()
        if not db_sess.query(User).filter(User.id == form.cooker.data).first():
            return render_template('dishes.html', title='Добавление новости',
                                   form=form,
                                   message="Шеф-повара с таким ID не существует")
        if not db_sess.query(Category).filter(Category.id == form.category.data).first():
            return render_template('dishes.html', title='Добавление новости',
                                   form=form,
                                   message="Категории с таким ID не существует")
        dish.title = form.title.data
        dish.cooker = form.cooker.data
        dish.work_size = form.work_size.data
        dish.category = form.category.data
        db_sess.add(dish)
        db_sess.commit()
        return redirect('/')
    return render_template('dishes.html', title='Добавление новости',
                           form=form)


@app.route('/add_dish/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dishes(id):
    form = DishesForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dish = db_sess.query(Dish).filter(Dish.id == id, ((Dish.user == current_user) | (current_user.id == 1))).first()
        if dish:
            form.title.data = dish.title
            form.cooker.data = dish.cooker
            form.work_size.data = dish.work_size
            form.ingredients.data = dish.ingredients
            form.category.data = dish.category
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dish = db_sess.query(Dish).filter(Dish.id == id, ((Dish.user == current_user) | (current_user.id == 1))).first()
        if not db_sess.query(Category).filter(Category.id == form.category.data).first():
            return render_template('dishes.html', title='Добавление новости',
                                   form=form,
                                   message="Категории с таким ID не существует")
        if dish:
            dish.title = form.title.data
            dish.cooker = form.cooker.data
            dish.work_size = form.work_size.data
            dish.ingredients = form.ingredients.data
            dish.category = form.category.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('dishes.html',
                           title='Добавление работы',
                           form=form)


@app.route('/dish_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def dish_delete(id):
    db_sess = db_session.create_session()
    dish = db_sess.query(Dish).filter(Dish.id == id, ((Dish.user == current_user) | (current_user.id == 1))).first()
    if dish:
        db_sess.delete(dish)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/like_it/<int:id>', methods=['GET', 'POST'])
@login_required
def like_it(id):
    db_sess = db_session.create_session()
    dish = db_sess.query(Dish).filter(Dish.id == id, ((Dish.user == current_user) | (current_user.id == 1))).first()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if current_user.is_authenticated:
        liked_dishes = list(map(lambda x: int(x) if 'None' not in x else 0, str(current_user.liked_dish).split(',')))
    else:
        liked_dishes = []
    if dish.id in liked_dishes:
        dish.likes -= 1
        del liked_dishes[liked_dishes.index(dish.id)]
    else:
        dish.likes += 1
        liked_dishes.append(str(dish.id))
    user.liked_dish = ', '.join([str(elem) for elem in liked_dishes])
    db_sess.commit()
    return redirect('/')


@app.route('/file_upload/<int:id>', methods=['POST', 'GET'])
def sample_file_upload(id):
    if request.method == 'GET':
        return render_template('file_upload.html', id=id)
    elif request.method == 'POST':
        f = request.files[str(id)]
        with open(f'static/img/{id}.jpg', 'wb') as s:
            s.write(f.read())
        return f'<a href="/" align="center">Форма отправлена. Вернуться на главную</a>'


@app.route('/')
def main():
    dishes = [elem for elem in db_sess.query(Dish).all()]
    if current_user.is_authenticated:
        liked_dishes = str(current_user.liked_dish).split(',')
    else:
        liked_dishes = []
    return render_template('table.html', orders_list=sorted(dishes, key=lambda x: x.likes, reverse=True), liked_dishes=liked_dishes)


if __name__ == '__main__':
    db_session.global_init("db/cook_or_buy.db")
    db_sess = db_session.create_session()
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(dishes_resource.DishesListResource, '/api/v2/dishes')
    api.add_resource(dishes_resource.DishesResource, '/api/v2/dishes/<int:dishes_id>')
    app.run(debug=True)