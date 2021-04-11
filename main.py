from flask import Flask, render_template, redirect, make_response, jsonify
from data import db_session
from data.users import User
from data.dishes import dish
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.add_job import JobsForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import reqparse, abort, Api, Resource
import users_resource
import jobs_resource

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
                                   message="Такой пользователь уже есть")
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


@app.route('/addjob',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dish = dishes()
        dish.dish = form.dish.data
        dish.team_leader = form.team_leader.data
        dish.work_size = form.work_size.data
        dish.collaborators = form.collaborators.data
        dish.is_finished = form.is_finished.data
        dish.category = form.category.data
        db_sess.add(dish)
        db_sess.commit()
        return redirect('/')
    return render_template('dishes.html', title='Добавление новости',
                           form=form)


@app.route('/')
def main():
    dishes = [elem for elem in db_sess.query(Dishes).all()]
    return render_template('table.html', orders__list=dishes)


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(jobs_resource.DishesListResource, '/api/v2/dishes')
    api.add_resource(jobs_resource.DishesResource, '/api/v2/dishes/<int:dishes_id>')
    app.run(debug=True)