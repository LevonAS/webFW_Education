"""
ORM
"""

from sqlite3 import connect

from .сreational_patterns import Category, Course, Student, Teacher, \
    CourseHavingStudent

connection = connect('learning.db')


class CategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'categories'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            cat_name = Category(id, name, category=None)
            # cat_name.id = id
            result.append(cat_name)
        return result

    def find_cat_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        result = result + (None,)
        print("// find_cat_by_id-result: ", result)
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CourseMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'courses'


    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, category_id = item
            course = Course(id, name, category_id)
            result.append(course)
        return result

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, category_id) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.name, obj.category_id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def courses_by_category(self, id):
        statement = f"SELECT id, name, category_id FROM {self.tablename} WHERE category_id=?"
        self.cursor.execute(statement, (id,))
        result = []
        for item in self.cursor.fetchall():
            course_item = Course(*item)
            print("///courses_by_category-course_item: ", course_item)
            result.append(course_item)
        return result  

    def find_by_id(self, id):
        statement = f"SELECT id, name, category_id FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        print("///course_by_id-result: ", result)
        if result:
            return Course(*result)
        else:
            raise RecordNotFoundException(f'record with category_id={id} not found')     

    def course_by_category(self, id):
        statement = f"SELECT id, name, category_id FROM {self.tablename} WHERE category_id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        print("///course_by_category-result: ", result)
        if result:
            return Course(*result)
        else:
            raise RecordNotFoundException(f'record with category_id={id} not found')

    def course_by_name(self, name):
        statement = f"SELECT id, name, category_id FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        print("///course_by_name-result: ", result)
        if result:
            return Course(*result)
        else:
            raise RecordNotFoundException(f'record with category_id={id} not found')


    def count_by_cat_id(self):
        statement = f'SELECT count(*) as course_count from {self.tablename} where category_id={id}'
        self.cursor.execute(statement)
        course_count=self.cursor.fetchall()
        return course_count 


class StudentMapper:
    """
    Паттерн DATA MAPPER
    Слой преобразования данных для модели Student
    """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'students'

    def all(self):
        statement = f'SELECT id, name from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(id, name)
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def student_by_name(self, name):
        statement = f"SELECT id, name FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        print("///student_by_name-result: ", result)
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with category_id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class TeacherMapper:
    pass


class CourseHavingStudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'course_student_association'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, course_id, student_id = item
            obj = CourseHavingStudent(id, course_id, student_id)
            
            result.append(obj)
        return result

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (course_id, student_id) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.course_id, obj.student_id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def courses_by_student(self, id):
        statement = f"SELECT course_id FROM {self.tablename} WHERE student_id=?"
        self.cursor.execute(statement, (id,))
        result = []
        for item in self.cursor.fetchall():
            obj = CourseMapper(self.connection).find_by_id(int(item[0]))
            print("///courses_by_student-obj: ", obj)
            result.append(obj)
        return result

    # def courses_by_student(self, id):
    #     statement = f"SELECT id, course_id, student_id FROM {self.tablename} WHERE student_id=?"
    #     self.cursor.execute(statement, (id,))
    #     result = []
    #     for item in self.cursor.fetchall():
    #         obj = CourseHavingStudent(*item)
    #         print("///courses_by_student-obj: ", obj)
    #         result.append(obj)
    #     return result

    def students_by_course(self, id):
        statement = f"SELECT student_id FROM {self.tablename} WHERE course_id=?"
        self.cursor.execute(statement, (id,))
        result = []
        for item in self.cursor.fetchall():
            obj = StudentMapper(self.connection).find_by_id(int(item[0]))
            print("///students_by_course-obj: ", obj)
            result.append(obj)
        return result

    def presence_check(self, obj):
        statement = f"SELECT id, course_id, student_id FROM {self.tablename} WHERE course_id=? and student_id=?"
        self.cursor.execute(statement, (obj.course_id, obj.student_id,))
        result = self.cursor.fetchone()
        print("///presence_check-result: ", result)
        if result:
            print(f'///presence_check: Такая запись уже существует')
            return CourseHavingStudent(*result)   
        else:
            print(f'///presence_check: Подобной записи ещё нет')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record in Db not found: {message}')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'category': CategoryMapper,
        'course': CourseMapper,
        'student': StudentMapper,
        'teacher': TeacherMapper,
        'course_student': CourseHavingStudentMapper     
    }

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Category):
            return CategoryMapper(connection)
        elif isinstance(obj, Course):
            return CourseMapper(connection)
        elif isinstance(obj, Student):
            return StudentMapper(connection)
        elif isinstance(obj, Teacher):
            return TeacherMapper(connection)
        elif isinstance(obj, CourseHavingStudent):
            return CourseHavingStudentMapper(connection)


if __name__ == '__main__':
    
    cat_mapper = CategoryMapper(connection)
    cat_all = cat_mapper.all()
    print("cat_all", cat_all)