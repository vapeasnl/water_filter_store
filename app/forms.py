from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ReviewForm(FlaskForm):
    body = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')
