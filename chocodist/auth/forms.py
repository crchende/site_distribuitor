from sqlalchemy import select, func
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, HiddenField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired, Length, Email, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from chocodist.date.modele import Utilizator
from chocodist.date.db import db

class LoginForm(FlaskForm):
    user = StringField("Utilizator", validators=[DataRequired(), Length(1, 64)])
    password = PasswordField("Parola", validators=[DataRequired()])
    remember_me = BooleanField("Pastreaza-ma logat")
    submit = SubmitField("Log In")

class RegisterForm(FlaskForm):
    user = StringField("Utilizator", validators=[
            DataRequired(), Length(3, 64),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, "Numele utilizatorului trebuie sa inceapa cu o litera si poate contine litere, cifre, '_' si '.'")
            ]
        )
    nume = StringField("Nume", validators=[DataRequired(), Length(1, 64)])
    prenume = StringField("Prenume", validators=[DataRequired(), Length(1, 64)])
    password = PasswordField("Parola", validators=[DataRequired(), Length(6, 64),
            EqualTo('password2', message='Parola nu este identica!')
            ]
        )
    password2 = PasswordField("Confirmare parola", validators=[DataRequired(), Length(6, 64)])
    submit = SubmitField("Inregistrare")

    def validate_user(self, field):
        u = db.session.scalar(select(Utilizator).where(Utilizator.nume_utilizator == field.data))
        if u:
            raise ValidationError("Numele de utilizator este deja folosit!")
        
        # permit doar un singur utilizator nevalidat (protectie - pt site-ul de pe web)
        u_nevalidati = db.session.scalar(select(func.count(Utilizator.id)).where(Utilizator.confirmat == None))
        if u_nevalidati > 0:
            raise ValidationError("""Contactati administratorul site-ului!
                                  Utilizatorul trebuie validat.
                                  (din moment ce ati ajuns aici probabil stiti cu cine trebuie sa vorbiti)""")