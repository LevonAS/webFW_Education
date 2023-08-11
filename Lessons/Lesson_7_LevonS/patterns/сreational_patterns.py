from copy import deepcopy
from quopri import decodestring

from .behavioral_patterns import FileWriter, Subject, SmsNotifier, EmailNotifier
from .architectural_system_pattern_unit_of_work import DomainObject
# from .data_mapper_patterns import MapperRegistry

# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# преподаватель
class Teacher(User, DomainObject):

    def __init__(self, teacher_id, name):
        super().__init__(name)
        self.teacher_id = teacher_id


# студент
class Student(User, DomainObject):

    def __init__(self, student_id, name):
        super().__init__(name)
        self.student_id = student_id


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](None, name)



class CourseHavingStudent(DomainObject):

    def __init__(self, id, course_id, student_id):
        self.course_id = course_id
        self.student_id = student_id


# порождающий паттерн Прототип - Курс
class CoursePrototype:
    # прототип курсов обучения

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject, DomainObject):

    def __init__(self, course_id, name, category_id):
        self.course_id = course_id
        self.name = name
        self.category_id = category_id
        # self.category.courses.append(self)
        # self.students = []
        super().__init__()

    # def __getitem__(self, item):
    #     return self.students[item]

    def add_student(self, student: Student):
        # course = MapperRegistry.get_current_mapper('course').course_by_name(course_name)
        
        return CourseHavingStudent(None, self.course_id, student.student_id)
        # if self.students.count(student):
        #     print(f"Студент {student.name} уже есть в списке")
        # else:
        #     self.students.append(student)
        #     # self.subject = self
        #     # self.observers.append(EmailNotifier())
        #     print("self.observers: ", self.observers)
        #     print("self.students: ", self.students)
            
        #     student.courses.append(self)
        #     self.notify()


# Интерактивный курс
class InteractiveCourse(Course):
    pass


# Курс в записи
class RecordCourse(Course):
    pass


# Категория
class Category(DomainObject):

    def __init__(self, category_id, name, category):
        self.category_id = category_id
        self.name = name
        self.category = category
        # self.courses = []

    # def course_count(self):
    #     result = len(self.courses)
    #     if self.category:
    #         result += self.category.course_count()
    #     return result


# порождающий паттерн Абстрактная фабрика - фабрика курсов
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category_id):
        return cls.types[type_](None, name, category_id)


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(None, name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def find_category_by_id_mapper(self, id):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.find_cat_by_id(id)

    
    def find_student_by_id(self, id):
        for item in self.students:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет студента с id = {id}')
    

    @staticmethod
    def create_course(type_, name, category_id):
        return CourseFactory.create(type_, name, category_id)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None
    
    def find_course_by_id(self, id):
        for item in self.courses:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет курса  с id = {id}')

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
        
