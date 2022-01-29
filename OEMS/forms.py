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

    subject = SelectField(label='Select Subject', choices=['None']+[], validators=[DataRequired()])
    department = SelectField(label='Filter by Department', choices=['All'] + [], validators=[DataRequired()])
    submit = SubmitField(label='Display Students')


class ViewStudentFormDept(FlaskForm):
    def validate_subject(self, subject_to_check):
        if subject_to_check == 'None':
            raise ValidationError('Select a subject to view students assigned')

    subject = SelectField(label='Select Subject', choices=['None']+[], validators=[DataRequired()])
    department = SelectField(label='Filter by Department', choices=['All'] + [], validators=[DataRequired()])
    submit = SubmitField(label='Display Students')


class AddElectiveForm(FlaskForm):
    def validate_teacher_code(self, tcode_to_check):
        if tcode_to_check == ('None', 'None'):
            raise ValidationError('Select a subject to view students assigned')

    subject_code = StringField(label='Subject Code', validators=[DataRequired(), Length(min=10, max=10)])
    elective_name = StringField(label='Elective Name', validators=[DataRequired()])
    teacher_code = SelectField(label='Teacher Code', choices=[('None', 'None')]+[], validators=[DataRequired()])
    submit = SubmitField(label='Add Elective')


class AddStudentForm(FlaskForm):
    def validate_teacher_code(self, tcode_to_check):
        if tcode_to_check == ('None', 'None'):
            raise ValidationError('Select a subject to view students assigned')

    usn = StringField(label='USN', validators=[DataRequired(), Length(min=10, max=10)])
    student_name = StringField(label='Student Name', validators=[DataRequired()])
    semester = StringField(label='Semester', validators=[DataRequired()])
    section = StringField(label='Section', validators=[DataRequired()])
    submit = SubmitField(label='Add Student')


class AddTeacherForm(FlaskForm):

    teacher_code = StringField(label='Teacher Code', validators=[DataRequired()])
    teacher_name = StringField(label='Teacher Name', validators=[DataRequired()])
    submit = SubmitField(label='Add Teacher')


class AddDepartmentForm(FlaskForm):
    
    department_code = StringField(label='Department Code', validators=[DataRequired()])
    department_name = StringField(label='Department Name', validators=[DataRequired()])
    submit = SubmitField(label='Add Department')
        