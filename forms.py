from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
import os

validInputSubstring = 'GitHub'


def CheckInput(form, field):
    if not os.path.isdir(field.data):
        raise ValidationError('Input is not a valid local directory!')


class InputRepoForm(FlaskForm):
    input = StringField('Repository Path:',
                        validators=[DataRequired(), CheckInput])

    select = SelectField('Select:',
                         choices=[('single', 'Single Commit'), ('fromTo', 'Between Commits'),
                                  ("sinceTo", "SinceTo")])

    commit1 = StringField('Commit1 :')

    commit2 = StringField('Commit 2:')

    date1 = StringField("Since")

    date2 = StringField("To")

    submit = SubmitField("Start")

    output = TextAreaField('Output')
