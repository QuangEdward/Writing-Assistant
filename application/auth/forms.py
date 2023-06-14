from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class MergeAccountForm(FlaskForm):
    field1 = StringField('Field 1', validators=[DataRequired()])
    field2 = StringField('Field 2', validators=[DataRequired()])
    submit = SubmitField('Merge Account')
