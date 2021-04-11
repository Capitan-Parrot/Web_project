from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class DishesForm(FlaskForm):
    title = StringField('Title of dish', validators=[DataRequired()])
    cooker = IntegerField("Cooker's ID", validators=[DataRequired()])
    work_size = IntegerField("Duration of cooking", validators=[DataRequired()])
    category = IntegerField("Category", validators=[DataRequired()])
    submit = SubmitField('Применить')
