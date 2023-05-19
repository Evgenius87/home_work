from datetime import datetime
from pprint import pprint

from sqlalchemy import and_, func, desc, select

from src.db import session
from src.models import Teacher, Student, Discipline, Group, Grade



# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_one():
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                    .select_from(Grade)\
                    .join(Student)\
                    .group_by(Student.id)\
                    .order_by(desc('avg_grade'))\
                    .limit(5).all()
    return result

# Знайти студента із найвищим середнім балом з певного предмета.
def select_two(discipline_id: int):
    result = session.query(Discipline.name, 
                           Student.fullname,
                           func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                    .select_from(Grade)\
                    .join(Student)\
                    .join(Discipline)\
                    .filter(Discipline.id == discipline_id)\
                    .group_by(Student.id, Discipline.name)\
                    .order_by(desc('avg_grade'))\
                    .limit(1).all()
    return result

# Знайти середній бал у групах з певного предмета.
def select_three(discipline_id: int, group_id: int):
    result = session.query(Group.name, Discipline.name , func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                        .select_from(Grade)\
                        .join(Student, Grade.student_id == Student.id)\
                        .join(Discipline, Grade.discipline_id == Discipline.id)\
                        .join(Group, Student.group_id == Group.id)\
                        .filter(and_(Discipline.id == discipline_id, Group.id == group_id))\
                        .group_by(Group.name, Discipline.name)\
                        .order_by(desc('avg_grade'))\
                        .all()
    return result

# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_four():
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                    .select_from(Grade)\
                    .all()
    return result                

# Знайти які курси читає певний викладач.
def select_five(teacher_id: int):
    result = session.query(Teacher.fullname, Discipline.name)\
                    .select_from(Discipline)\
                    .join(Teacher, Discipline.teacher_id == Teacher.id)\
                    .filter(Teacher.id == teacher_id)\
                    .order_by(Discipline.name)\
                    .all()
    return result

# Знайти список студентів у певній групі.
def select_six(group_id: int):
    result = session.query(Student.fullname)\
                    .select_from(Student)\
                    .join(Group)\
                    .filter(Group.id == group_id)\
                    .group_by(Student.fullname)\
                    .all()
    return result

# Знайти оцінки студентів у окремій групі з певного предмета.
def select_seven(group_id: int, discipline_id: int):
    result = session.query(Student.fullname, Grade.grade)\
                    .select_from(Grade)\
                    .join(Student, Grade.student_id == Student.id)\
                    .join(Discipline, Grade.discipline_id == Discipline.id)\
                    .join(Group, Student.group_id == Group.id)\
                    .filter(and_(Group.id == group_id, Discipline.id == discipline_id))\
                    .order_by(Grade.date_of)\
                    .all()
    return result

# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_eight(teacher_id: int, discipline_id: int):
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                    .select_from(Grade)\
                    .join(Discipline)\
                    .join(Teacher)\
                    .filter(and_(Teacher.id == teacher_id, Discipline.id == discipline_id))\
                    .order_by(desc('avg_grade'))\
                    .all()
    return result

# Знайти список курсів, які відвідує певний студент.
def select_nine(student_id: int):
    result = session.query(Discipline.name)\
                    .select_from(Grade)\
                    .join(Discipline)\
                    .join(Student)\
                    .filter(Student.id == student_id)\
                    .group_by(Discipline.name)\
                    .all()
    return result

# Список курсів, які певному студенту читає певний викладач.
def select_ten(student_id: int, teacher_id: int):
    result = session.query(Discipline.name)\
                    .select_from(Grade)\
                    .join(Discipline)\
                    .join(Teacher)\
                    .join(Student)\
                    .filter(and_(Teacher.id == teacher_id, Student.id == student_id))\
                    .group_by(Discipline.name)\
                    .all()
    return result

# Середній бал, який певний викладач ставить певному студентові.
def select_eleven(teacher_id: int, student_id: int):
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                    .select_from(Grade)\
                    .join(Discipline)\
                    .join(Teacher)\
                    .join(Student)\
                    .filter(and_(Teacher.id == teacher_id, Student.id == student_id))\
                    .order_by(desc('avg_grade'))\
                    .all()
    return result

# Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_last(discipline_id: int, group_id: int):
    subquery = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == discipline_id, Group.id == group_id)
    ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery())
    
    result = session.query(Discipline.name, 
                           Student.fullname,
                           Group.name,
                           Grade.date_of,
                           Grade.grade,
                           )\
                    .select_from(Grade)\
                    .join(Student)\
                    .join(Discipline)\
                    .join(Group)\
                    .filter(and_(Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery))\
                    .order_by(desc(Grade.date_of))\
                    .all()
    return result

if __name__ == "__main__":
    pprint(select_one()[0])
    # pprint(select_two(1))
    # pprint(select_three(1, 1))
    # pprint(select_four())
    # pprint(select_five(1))
    # pprint(select_six(1))
    # pprint(select_seven(1, 1))
    # pprint(select_eight(1, 1))
    # pprint(select_nine(1))
    # pprint(select_ten(1, 1))

    # pprint(select_eleven(1, 1))
    # pprint(select_last(1, 1))