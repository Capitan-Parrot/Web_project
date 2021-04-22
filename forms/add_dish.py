from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField, SubmitField, IntegerField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired


class DishesForm(FlaskForm):
    title = StringField('Название блюда', validators=[DataRequired()])
    cooker = IntegerField("ID Шеф-повара", validators=[DataRequired()])
    work_size = StringField("Длительность приготовления", validators=[DataRequired()])
    ingredients = StringField("Ингредиенты", validators=[DataRequired()])
    category = IntegerField("ID Категории блюда", validators=[DataRequired()])
    recipe = TextAreaField("Рецепт", validators=[DataRequired()])
    submit = SubmitField('Применить')
