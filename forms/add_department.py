from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class DepartmentsForm(FlaskForm):
    title = StringField('Title of department', validators=[DataRequired()])
    chief = IntegerField("Chief's ID", validators=[DataRequired()])
    members = StringField("Members")
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Применить')
