from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

currency_choices = [('USD', 'US Dollar'), ('AUD', 'Australian Dollar'), ('JPY', 'Japanese Yen')]

class UserRegistration(FlaskForm):
    '''form for registering user'''
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserProfile(FlaskForm):
    '''form for editing user preferences'''
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    currency = SelectField(label='Currency', choices=currency_choices)

class LoginForm(FlaskForm):
    '''form for logging in'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])