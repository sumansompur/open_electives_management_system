from cgitb import reset
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from OEMS.models import Elective, Student, Teacher, User, Department
from OEMS import db, cursor

class LoginForm(FlaskForm):
    user_id = StringField(label='User ID (USN / DEPT Name / Teacher ID):', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class RegisterForm(FlaskForm):
    def validate_user_id(self, userid_to_check):
        user = User.check_if_user_exists(user_id_to_check=userid_to_check.data)
        if user != None:
            raise ValidationError('Username already exists! Please try a different username')
        if self.user_type.data == 'Student':
            cursor.execute(f"select usn from student where usn='{self.user_id.data}'")
            result = cursor.fetchall()
            if result == []:
                raise ValidationError('No such USN Exists, Please Contact your respective department')
        if self.user_type.data == 'Teacher':
            cursor.execute(f"select teacher_code from teacher where teacher_code='{self.user_id.data}'")
            result = cursor.fetchall()
            if result == []:
                raise ValidationError('No such Teacher Exists, Please Contact your respective department')

    def validate_email_address(self, email_address_to_check):
        email_address = User.check_if_email_exists(email_id_to_check=email_address_to_check.data)
        if email_address != None:
            raise ValidationError('Email Address already exists! Please try a different email address')

    user_id = StringField(label='User ID', validators=[DataRequired(), Length(min=5, max=10)])
    username = StringField(label='Full Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    user_type = SelectField(label='Choose role', choices = ['Student', 'Teacher'], validators = [DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class ViewStudentForm(FlaskForm):
    subject = SelectField(label='Select Subject', choices=['All'], validators=[DataRequired()])
    submit = SubmitField(label='Display Students')


class ViewStudentFormDept(FlaskForm):
    subject = SelectField(label='Select Subject', choices=['All'], validators=[DataRequired()])
    submit = SubmitField(label='Display Students')


class AddElectiveForm(FlaskForm):
    def validate_subject_code(self, ecode_to_check):
        result = Elective.check_if_elective_exists(ecode_to_check.data)
        if result != None:
            raise ValidationError("Elective already exists!")

    subject_code = StringField(label='Subject Code', validators=[DataRequired(), Length(min=6, max=10)])
    elective_name = StringField(label='Elective Name', validators=[DataRequired()])
    teacher_code = SelectField(label='Teacher Code', choices=[], validators=[DataRequired()])
    submit = SubmitField(label='Add Elective')


class AddStudentForm(FlaskForm):
    def validate_usn(self, usn_to_check):
        result = Student.check_if_student_exists(usn_to_check.data)
        if result != None:
            raise ValidationError("Student USN already exists!")

    usn = StringField(label='USN', validators=[DataRequired(), Length(min=10, max=10)])
    student_name = StringField(label='Student Name', validators=[DataRequired()])
    semester = StringField(label='Semester', validators=[DataRequired()])
    section = StringField(label='Section', validators=[DataRequired()])
    submit = SubmitField(label='Add Student')


class AddTeacherForm(FlaskForm):
    def validate_teacher_code(self, tcode_to_check):
        result = Teacher.check_if_teacher_exists(tcode_to_check.data)
        if result != None:
            raise ValidationError("Teacher already exists!")
    
    teacher_code = StringField(label='Teacher Code', validators=[DataRequired()])
    teacher_name = StringField(label='Teacher Name', validators=[DataRequired()])
    submit = SubmitField(label='Add Teacher')


class AddDepartmentForm(FlaskForm):
    def validate_department_code(self, code_to_check):
        result = Department.check_if_department_exists(code_to_check.data)
        if result != None:
            raise ValidationError('Department already exists!')

    department_code = StringField(label='Department Code', validators=[DataRequired()])
    department_name = StringField(label='Department Name', validators=[DataRequired()])
    submit = SubmitField(label='Add Department')
        
class AddUserForm(FlaskForm):
    def validate_user_id(self, userid_to_check):
        user = User.check_if_user_exists(user_id_to_check=userid_to_check.data)
        if user != None:
            raise ValidationError('Username already exists! Please try a different username')
        if self.user_type.data == 'Student':
            cursor.execute(f"select usn from student where usn='{self.user_id.data}'")
            result = cursor.fetchall()
            if result == []:
                raise ValidationError('No such USN Exists, Please Contact department')
        if self.user_type.data == 'Teacher':
            cursor.execute(f"select teacher_code from teacher where teacher_code='{self.user_id.data}'")
            result = cursor.fetchall()
            if result == []:
                raise ValidationError('No such Teacher Exists, Please Contact department')
        if self.user_type.data == 'Department':
            cursor.execute(f"select department_code from department where department_code='{self.user_id.data}'")
            result = cursor.fetchall()
            if result == []:
                raise ValidationError('No such Department Exists, Please Add the department to create such user')        


    def validate_email_address(self, email_address_to_check):
        email_address = User.check_if_email_exists(email_id_to_check=email_address_to_check.data)
        if email_address != None:
            raise ValidationError('Email Address already exists! Please try a different email address')

    user_id = StringField(label='User ID', validators=[DataRequired(), Length(min=3, max=10)])
    username = StringField(label='Full Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    user_type = SelectField(label='Choose role', choices = ['Student', 'Teacher', 'Department', 'Admin'], validators = [DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Add User')

class FilterUserForm(FlaskForm):
    subject = SelectField(label='Select Privileges', choices=['All', 'Student', 'Teacher', 'Department', 'Admin'], validators=[DataRequired()])
    submit = SubmitField(label='Display Students')