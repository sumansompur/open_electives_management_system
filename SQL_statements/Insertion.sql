insert into department values('CSE', 'Computer Science and Engineering');
insert into department values('ISE', 'Information Science and Engineering');

insert into open_elective(subject_code, elective_name, department_code) values('18CS61', 'ABCD', 'CSE');
insert into open_elective(subject_code, elective_name, department_code) values('18CS62', 'ABCDE', 'CSE');

insert into student values('1BI19CS159', 'Suman', 5, 'C', '18CS61', 'CSE');
insert into student values('1BI19CS158', 'Sujan', 5, 'C', '18CS62', 'CSE');

insert into teacher values('BI101', 'MCV', 'CSE');
insert into teacher values('BI102', 'MBV', 'CSE');

insert into users values('admin', 'Admin', 'admin.bit@gmail.com', 'admin', 'admin');
insert into users values('student', 'Student', 'student.bit@gmail.com', 'student', 'stdnt');

