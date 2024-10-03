from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Login')
    
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField('Signup')
    
class CreatePortfolioForm(FlaskForm):
    name = StringField('Portfolio Name', validators=[DataRequired()])
    submit = SubmitField('Create')
    
class AddStockForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired()])
    cost = FloatField('Cost Per Share', validators=[DataRequired()])
    shares = FloatField('Shares', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Add')