from crypt import methods
from random import choice
from time import sleep

from sqlalchemy import delete
from OEMS import app
from flask import jsonify, render_template, redirect, url_for, flash, request
from OEMS.forms import AddUserForm, AddDepartmentForm, AddTeacherForm, AddStudentForm, DeleteForm, EditForm, LoginForm, RegisterForm, SelectElective, ViewStudentForm, ViewStudentFormDept, AddElectiveForm
from OEMS.forms import FilterUserForm
from OEMS.models import Department, Elective, Student, Teacher, User
from OEMS import db, cursor
from flask_login import login_user, logout_user, login_required, current_user

#HOME ROUTES
@app.route('/')
@app.route('/home/')
def home_page():
    return render_template('home.html')


@app.route('/login/', methods = ['GET', 'POST'])
def login_page():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('user_routing'))
    if form.validate_on_submit():
        attempted_user = User.check_if_user_exists(form.user_id.data)
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {current_user.user_name}', category='success')
            return redirect(url_for('user_routing'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(form.user_id.data, form.username.data, form.email_address.data, user_privileges=form.user_type.data, password_hash=form.password1.data)
        user_to_create.commit()
        flash(f"Account created successfully! You can now log in.", category='success')
        return redirect(url_for('login_page'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/user/')
def user_routing():
    sleep(0.5)
    if current_user.user_privileges == 'Student':
        return redirect(url_for('student_page'))
    elif current_user.user_privileges == 'Admin':    
        return redirect(url_for('admin_page'))
    elif current_user.user_privileges == 'Department':    
        return redirect(url_for('department_page'))
    elif current_user.user_privileges == 'Teacher':    
        return redirect(url_for('view_students'))    




#DEPARTMENT ROUTES
@app.route('/user/department/')
@login_required
def department_page():
    if current_user.user_privileges == 'Department':
        return render_template('department.html')
    else:
        return redirect(url_for('user_routing'))



@app.route('/user/department/manage-electives/', methods = ['GET', 'POST'])
@login_required
def manage_electives():
    if current_user.user_privileges == 'Department':
        cursor.execute(f"select o.*, t.tname from open_elective as o, teacher t where o.department_code='{current_user.user_id}' and t.teacher_code=o.teacher_code order by subject_code")
        result = cursor.fetchall()
        form=AddElectiveForm()
        deleteForm = DeleteForm()
        editForm = EditForm()
        cursor.execute(f"select t.teacher_code, t.tname from teacher t where department_code='{current_user.user_id}'")
        sub_query = cursor.fetchall()
        teachers = [item for item in sub_query]
        form.teacher_code.choices = teachers
        if form.validate_on_submit() and form.submit.data:
            choice = form.teacher_code.data
            choice = choice.strip('()').split(',')
            elective = Elective(form.subject_code.data, form.elective_name.data, current_user.user_id, choice[0])
            elective.commit()
            flash(f"Elective added successfully!", category='success')
            return redirect(url_for('manage_electives'))
        
        elif deleteForm.validate_on_submit() and deleteForm.delete.data:
            subject_code = request.form.get('deleted_item')
            Elective.delete(subject_code, current_user.user_id)
            flash(f'Elective: {subject_code} deleted successfully', category='warning')
            return redirect(url_for('manage_electives'))

        elif editForm.validate_on_submit() and editForm.edit.data:
            subcode = request.form.get('subcode')
            ename = request.form.get('ename')
            teacher_code = request.form.get('teacher_code')
            teacher_code = teacher_code.strip('()').split(',')
            Elective.update(subcode, ename, teacher_code[0])
            flash(f"Update Successful!", category='info')
            return redirect(url_for('manage_electives'))  

        if form.errors != {}: #If there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error with adding elective: {err_msg}', category='danger')
        
        return render_template('dept_electives.html', form=form, query=result, deleteForm=deleteForm, editForm=editForm, list=teachers)
    else:
        return redirect(url_for('user_routing'))


@app.route('/user/department/manage-students/', methods = ['GET', 'POST'])
@login_required
def manage_students():
    if current_user.user_privileges == 'Department':
        cursor.execute(f"select * from student where department_code='{current_user.user_id}' order by usn")
        result = cursor.fetchall()
        form = AddStudentForm()
        deleteForm = DeleteForm()
        editForm = EditForm()
        if form.validate_on_submit() and form.submit.data:
            student = Student(form.usn.data, form.student_name.data, form.semester.data, form.section.data, current_user.user_id)
            student.commit()
            flash(f"Student Added Successfully!", category='success')
            return redirect(url_for('manage_students'))
        elif deleteForm.validate_on_submit() and deleteForm.delete.data:
            code = request.form.get('deleted_item')
            Student.delete(code)
            flash(f'Student: {code} deleted successfully', category='warning')
            return redirect(url_for('manage_students'))
        elif editForm.validate_on_submit() and editForm.edit.data:
            usn = request.form.get('usn')
            sname = request.form.get('sname')
            semester = request.form.get('semester')
            section = request.form.get('section')
            Student.update(usn, sname, semester, section)
            flash(f"Update Successful!", category='info')
            return redirect(url_for('manage_students'))

        if form.errors != {}: #If there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}', category='danger')
        
        return render_template('dept_students.html', form=form, query=result, deleteForm=deleteForm, editForm=editForm)
    else:
        return redirect(url_for('user_routing'))


@app.route('/user/department/manage-teachers/', methods = ['GET', 'POST'])
@login_required
def manage_teachers():
    if current_user.user_privileges == 'Department':
        cursor.execute(f"select t.teacher_code, t.tname from teacher t where t.department_code='{current_user.user_id}' order by teacher_code")
        result = cursor.fetchall()
        form = AddTeacherForm()
        deleteForm = DeleteForm()
        editForm = EditForm()
        if form.validate_on_submit() and form.submit.data:
            teacher = Teacher(form.teacher_code.data, form.teacher_name.data, current_user.user_id)
            teacher.commit()
            flash(f"Teacher Added Successfully!", category='success')
            return redirect(url_for('manage_teachers'))
        elif deleteForm.validate_on_submit() and deleteForm.delete.data:
            code = request.form.get('deleted_item')
            Teacher.delete(code)
            flash(f'Teacher: {code} deleted successfully', category='warning')
            return redirect(url_for('manage_teachers'))
        elif editForm.validate_on_submit() and editForm.edit.data:
            teacher_code = request.form.get('teacher_code')
            tname = request.form.get('tname')
            Teacher.update(teacher_code, tname)
            flash(f"Update Successful!", category='info')
            return redirect(url_for('manage_teachers'))

        if form.errors != {}: #If there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}', category='danger')
        return render_template('dept_teachers.html', form=form, query=result, deleteForm=deleteForm, editForm=editForm)
    else:
        return redirect(url_for('user_routing'))



@app.route('/user/department/view-students/', methods=['GET', 'POST'])
@login_required
def dept_view_students():
    if current_user.user_privileges == 'Department':
        cursor.execute(f"select s.* from student as s, open_elective as o where s.subject_code=o.subject_code and o.department_code='{current_user.user_id}' order by usn, subject_code")
        result = cursor.fetchall()
        form = ViewStudentFormDept()
        cursor.execute(f"select subject_code, elective_name from open_elective where department_code='{current_user.user_id}'")
        sub_query = cursor.fetchall()
        subjects = [item for item in sub_query]
        form.subject.choices += subjects
        if form.validate_on_submit():
            if form.subject.data != 'All':
                choice = form.subject.data
                choice = choice.strip('()').split(',')
                print(choice)
                cursor.execute(f"select s.* from student as s, open_elective as o where s.subject_code=o.subject_code and o.department_code='{current_user.user_id}' and o.subject_code={choice[0]} order by usn")
                result = cursor.fetchall()
                print(result)
            else:
                cursor.execute(f"select s.* from student as s, open_elective as o where s.subject_code=o.subject_code and o.department_code='{current_user.user_id}' order by usn, subject_code")
                result = cursor.fetchall()
                print(result)
            return render_template('view_students.html', form=form, query=result)
        return render_template('view_students.html', form=form, query=result)
    else:
        return redirect(url_for('user_routing'))
    





#ADMIN ROUTES
@app.route('/user/admin/')
@login_required
def admin_page():
    if current_user.user_privileges == 'Admin':
        return render_template('admin.html')
    else:
        return redirect(url_for('user_routing'))


@app.route('/user/admin/manage-departments/', methods = ['GET', 'POST'])
@login_required
def admin_manage_departments():
    if current_user.user_privileges == 'Admin':
        cursor.execute(f"select * from department")
        result = cursor.fetchall()
        form=AddDepartmentForm()
        deleteForm = DeleteForm()
        editForm = EditForm()

        if form.validate_on_submit() and form.submit.data:
            department = Department(form.department_code.data, form.department_name.data)
            department.commit()
            flash(f"Department created successfully!", category='success')
            return redirect(url_for('admin_manage_departments'))

        elif deleteForm.validate_on_submit() and deleteForm.delete.data:
            code = request.form.get('deleted_item')
            Department.delete(code)
            flash(f'Department {code} deleted successfully', category='warning')
            return redirect(url_for('admin_manage_departments'))

        elif editForm.validate_on_submit() and editForm.edit.data:
            department_code = request.form.get('department_code')
            department_name = request.form.get('department_name')
            print(department_code, department_name)
            Department.update(department_code, department_name)
            flash(f"Update Successful!", category='info')
            return redirect(url_for('admin_manage_departments'))

        if form.errors != {}: 
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}', category='danger') 

        return render_template('admin_depts.html', form=form, query=result, deleteForm=deleteForm, editForm=editForm)
    else:
        return redirect(url_for('user_routing'))
    

@app.route('/user/admin/manage-users/', methods = ['GET', 'POST'])
@login_required
def admin_manages_users():
    if current_user.user_privileges == 'Admin':
        cursor.execute(f"select u.user_id, u.user_name, u.email, u.user_privileges from users as u")
        result = cursor.fetchall()
        filter = FilterUserForm()
        deleteForm = DeleteForm()
        
        form=AddUserForm()
        if filter.validate_on_submit():
            if filter.subject.data != 'All':
                choice = filter.subject.data
                print(choice)
                cursor.execute(f"select u.user_id, u.user_name, u.email, u.user_privileges from users as u where u.user_privileges='{choice}'")
                result = cursor.fetchall()
                print(result)
            else:
                cursor.execute(f"select u.user_id, u.user_name, u.email, u.user_privileges from users as u")
                result = cursor.fetchall()
                print(result)
            return render_template('admin_users.html', form=form, query=result, filter=filter, deleteForm=deleteForm)

        if form.validate_on_submit():
            user_to_create = User(form.user_id.data, form.username.data, form.email_address.data, user_privileges=form.user_type.data, password_hash=form.password1.data)
            user_to_create.commit()
            flash(f"User created successfully!", category='success')
            return redirect(url_for('admin_manages_users'))
        
        if deleteForm.validate_on_submit():
            code = request.form.get('deleted_item')
            User.delete(code, current_user.user_id)
            flash(f'User: {code} deleted successfully', category='warning')
            return redirect(url_for('admin_manages_users'))

        if form.errors != {}: #If there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}', category='danger') 
            
        return render_template('admin_users.html', form=form, query=result, filter=filter, deleteForm=deleteForm)
    else:
        return redirect(url_for('user_routing'))







#TEACHER ROUTES
@app.route('/user/teacher', methods=['GET', 'POST'])
def view_students():
    if current_user.user_privileges == 'Teacher':
        cursor.execute(f"select s.* from student as s, open_elective as o where s.subject_code=o.subject_code and o.teacher_code='{current_user.user_id}' order by usn, subject_code")
        result = cursor.fetchall()
        form = ViewStudentForm()
        cursor.execute(f"select subject_code, elective_name from open_elective where teacher_code='{current_user.user_id}'")
        sub_query = cursor.fetchall()
        subjects = [item for item in sub_query]
        form.subject.choices += subjects
        if form.validate_on_submit():
            if form.subject.data != 'All':
                choice = form.subject.data
                choice = choice.strip('()').split(',')
                print(choice)
                cursor.execute(f"select s.* from student as s, open_elective as o where s.subject_code=o.subject_code and o.teacher_code='{current_user.user_id}' and o.subject_code={choice[0]} order by usn")
                result = cursor.fetchall()
                print(result)
            else:
                cursor.execute(f"select s.* from student as s, open_elective as o where s.subject_code=o.subject_code and o.teacher_code='{current_user.user_id}' order by usn, subject_code")
                result = cursor.fetchall()
                print(result)
            return render_template('teacher.html', form=form, query=result)
        return render_template('teacher.html', form=form, query=result)
    else:
        return redirect(url_for('user_routing'))


#STUDENT ROUTES
@app.route('/user/student/', methods=['GET', 'POST'])
@login_required
def student_page():
    if current_user.user_privileges == 'Student':
        cursor.execute(f"select o.subject_code, o.elective_name from student s, open_elective o where s.usn='{current_user.user_id}' and s.subject_code=o.subject_code")
        data1 = cursor.fetchall()
        student = Student.check_if_student_exists(current_user.user_id)
        form = SelectElective()
        cursor.execute(f"select department_code from department where department_code<>'{student.department_code}'")
        result = cursor.fetchall()
        result = [item[0] for item in result]
        form.department.choices += result
        cursor.execute(f"select subject_code, elective_name from open_elective where department_code='{result[0]}'")
        electives = cursor.fetchall()
        electives = [(item[0], item[0] + '-' + item[1]) for item in electives]
        form.elective.choices += electives

        if request.method=='POST':
            print(form.elective.data)
            cursor.execute(f"update student set subject_code='{form.elective.data}' where usn='{current_user.user_id}'")
            db.commit()
            flash("Changed elective Successfully!", category='warning')
            return redirect(url_for('student_page'))
        
        return render_template('student.html', data=student, form=form, data1=data1)
    else:
        return redirect(url_for('user_routing'))

@app.route('/user/student/ele/<department>')
@login_required
def dept(department):
    cursor.execute(f"select subject_code, elective_name from open_elective where department_code='{department}'")
    result = cursor.fetchall()
    result = [item for item in result]

    array = []
    for item in result:
        obj = {}
        obj['id'] = item[0]
        obj['name'] = item[1]
        array.append(obj)
    
    return jsonify({'subs' : array})
    



































'''
@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')


        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')

   return redirect(url_for("home_page"))
'''









