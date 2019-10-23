from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from myblog.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=6, max=20)])
    confirm_password = PasswordField("Confirm password", validators=[
        DataRequired(), EqualTo('password')
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if user:
            raise ValidationError("That username is taken."
                                  "Please choose different one")
