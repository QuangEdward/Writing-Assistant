# application/grammar_check/forms.py
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    input_text = TextAreaField('Enter your text:', validators=[DataRequired()])
    paraphrase = SubmitField('Submit')