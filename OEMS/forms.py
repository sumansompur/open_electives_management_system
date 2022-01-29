from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
#from OEMS.models import User

class LoginForm(FlaskForm):
    user_id = StringField(label='User ID (USN / DEPT Name / Teacher ID):', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class RegisterForm(FlaskForm):
    def validate_user_id(self, userid_to_check):
        user = None
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = None
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    user_id = StringField(label='User ID', validators=[DataRequired(), Length(min=5, max=10)])
    username = StringField(label='Full Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    user_type = SelectField(label='Choose role', choices = ['Student', 'Teacher'], validators = [DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class ViewStudentForm(FlaskForm):
    def validate_subject(self, subject_to_check):
        if subject_to_check == 'None':
            raise ValidationError('Select a subject to view students assigned')

    subject = SelectField(label='Select Subject', choices=[None]+[], validators=[DataRequired()])
    department = SelectField(label='Filter by Department', choices=['All'] + [], validators=[DataRequired()])
    submit = SubmitField(label='Display Students')



'''



class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')
'''