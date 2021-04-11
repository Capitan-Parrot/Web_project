from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Title of activity', validators=[DataRequired()])
    team_leader = IntegerField("Leader's ID", validators=[DataRequired()])
    work_size = IntegerField("Duration", validators=[DataRequired()])
    collaborators = StringField('List of collaborators')
    category = IntegerField("Category", validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Применить')
