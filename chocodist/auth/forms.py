from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, HiddenField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired, Length, Email, Regexp, EqualTo, NumberRange
from wtforms import ValidationError

class LoginForm(FlaskForm):
    user = StringField("Utilizator", validators=[DataRequired(), Length(1, 64)])
    password = PasswordField("Parola", validators=[DataRequired()])
    remember_me = BooleanField("Pastreaza-ma logat")
    submit = SubmitField("Log In")