create table department(
department_code varchar(5),
department_name varchar(40),
constraint pk_dept_code primary key(department_code));

create table teacher(
teacher_code varchar(10),
tname varchar(25),
department_code varchar(5),
constraint pk_teacher_code primary key(teacher_code),
constraint fk_teacher_dept_code foreign key(department_code) references department(department_code));

create table open_elective(
subject_code varchar(8),
elective_name varchar(25),
department_code varchar(5),
teacher_code varchar(10) default null,
constraint pk_oe_sc primary key(subject_code),
constraint fk_oe_dept_code foreign key(department_code) references department(department_code),
constraint fk_oe_teach_code foreign key(teacher_code) references teacher(teacher_code) on delete set null);

create table student(
usn varchar(10),
sname varchar(25),
semester int,
section char(1),
subject_code varchar(8),
department_code varchar(5),
constraint pk_student primary key(usn),
constraint fk_stu_sub foreign key(subject_code) references open_elective(subject_code),
constraint fk_stu_dcode foreign key(department_code) references department(department_code));

create table users(
user_id varchar(15),
user_name varchar(25),
email varchar(30),
password_hash varchar(100),
user_privileges varchar(5),
constraint pk_users primary key(user_id));
