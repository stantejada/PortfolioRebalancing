from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Login')
    
    
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
    repeat_password = PasswordField('password', validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField('Signup')
    