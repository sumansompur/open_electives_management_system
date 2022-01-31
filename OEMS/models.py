from flask import flash
from OEMS import login_manager
from OEMS import bcrypt
from flask_login import UserMixin, current_user
from OEMS import db, cursor


@login_manager.user_loader
def load_user(user_id):
    cursor.execute(f"select * from users where user_id ='{user_id}'")
    result = cursor.fetchone()
    return User(result[0], result[1], result[2], result[3], result[4])

class User(UserMixin):
    def __init__(self, user_id, user_name, email, password_hash, user_privileges):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.password_hash = password_hash
        self.user_privileges = user_privileges

    '''
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    '''
    
    def check_password_correction(self, attempted_password):
        return self.password_hash == attempted_password

    def check_if_user_exists(user_id_to_check):
        cursor.execute(f"select * from users where user_id='{user_id_to_check}'")
        result = cursor.fetchall()
        if result != []:
            return User(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
        else:
            return None

    def check_if_email_exists(email_id_to_check):
        cursor.execute(f"select * from users where email='{email_id_to_check}'")
        result = cursor.fetchall()
        if result != []:
            return User(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
        else:
            return None

    def commit(self):
        cursor.execute(f"insert into users values('{self.user_id}', '{self.user_name}', '{self.email}', '{self.password_hash}', '{self.user_privileges}')")
        db.commit()
    
    def delete(user_id, current_user_id):
        if current_user_id != user_id:
            cursor.execute(f"delete from users where user_id='{user_id}'")
            db.commit()
            return 'success'
        else:
            return 'failure'
    
    def get_id(self):
        return self.user_id
        
class Department:
    def __init__(self, department_code, department_name):
        self.department_code = department_code
        self.department_name = department_name

    def commit(self):
        cursor.execute(f"insert into department values('{self.department_code}', '{self.department_name}')")
        db.commit()
    
    def check_if_department_exists(department_code_to_check):
        cursor.execute(f"select * from department where department_code='{department_code_to_check}'")
        result = cursor.fetchall()
        if result != []:
            return Department(result[0][0], result[0][1])
        else:
            return None

    def delete(department_code):
        cursor.execute(f"delete from department where department_code='{department_code}'")
        db.commit()
    
    def update(department_code, department_name):
        cursor.execute(f"update department set department_name='{department_name}' where department_code='{department_code}'")
        db.commit()

class Elective:
    def __init__(self, subject_code, elective_name, department_code, teacher_code):
        self.subject_code = subject_code
        self.elective_name = elective_name
        self.department_code = department_code
        self.teacher_code = teacher_code

    def commit(self):
        cursor.execute(f"insert into open_elective values('{self.subject_code}', '{self.elective_name}', '{self.department_code}', '{self.teacher_code}')")
        db.commit()

    def check_if_elective_exists(subject_code_to_check):
        print(current_user.user_id)
        cursor.execute(f"select * from open_elective where subject_code='{subject_code_to_check}' and department_code='{current_user.user_id}'")
        result = cursor.fetchall()
        if result != []:
            return Elective(result[0][0], result[0][1], result[0][2], result[0][3])
        else:
            return None

    def delete(subject_code, department_code):
        cursor.execute(f"delete from open_elective where subject_code='{subject_code}' and department_code='{department_code}'")
        db.commit()  

    def update(subcode, ename, teacher_code):  
        cursor.execute(f"update open_elective set elective_name='{ename}', teacher_code={teacher_code} where subject_code='{subcode}'")
        db.commit()

class Student:
    def __init__(self, usn, sname, semester, section, department_code):
        self.usn = usn
        self.sname = sname
        self.semester = semester
        self.section = section
        self.department_code = department_code

    def commit(self):
        cursor.execute(f"insert into student(usn,sname,semester,section,department_code) values('{self.usn}', '{self.sname}' , {self.semester}, '{self.section}', '{self.department_code}');")
        db.commit()
    
    def check_if_student_exists(usn_to_check):
        cursor.execute(f"select usn,sname,semester,section,department_code from student where usn='{usn_to_check}'")
        result = cursor.fetchall()
        if result != []:
            return Student(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
        else:
            return None
    
    def delete(usn):
        cursor.execute(f"delete from student where usn='{usn}'")
        db.commit()
    
    def update(usn, sname, semester, section):
        cursor.execute(f"update student set sname='{sname}', semester={semester}, section='{section}' where usn='{usn}'")
        db.commit()

class Teacher:
    def __init__(self, teacher_code, tname, department_code):
        self.teacher_code = teacher_code
        self.tname = tname
        self.department_code = department_code

    def commit(self):
        cursor.execute(f"insert into teacher values('{self.teacher_code}', '{self.tname}', '{self.department_code}')")
        db.commit()
    
    def check_if_teacher_exists(teacher_code_to_check):
        cursor.execute(f"select * from teacher where teacher_code='{teacher_code_to_check}'")
        result = cursor.fetchall()
        if result != []:
            return Teacher(result[0][0], result[0][1], result[0][2])
        else:
            return None

    def delete(teacher_code):
        cursor.execute(f"delete from teacher where teacher_code='{teacher_code}'")
        db.commit()  

    def update(teacher_code, new_name):
        cursor.execute(f"update teacher set tname='{new_name}' where teacher_code='{teacher_code}'")
        db.commit()
        


    
        