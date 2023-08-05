from copy import deepcopy
from quopri import decodestring
from .behavioral_patterns import FileWriter, Subject, SmsNotifier, EmailNotifier


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# преподаватель
class Teacher(User):
    pass


# студент
class Student(User):
    auto_id = 0

    def __init__(self, name):       
        self.id = Student.auto_id
        Student.auto_id += 1
        super().__init__(name)
        self.courses = []


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн Прототип - Курс
class CoursePrototype:
    # прототип курсов обучения

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    auto_id = 0

    def __init__(self, name, category):
        self.id = Course.auto_id
        Course.auto_id += 1
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        # self.attach(EmailNotifier())      
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        if self.students.count(student):
            print(f"Студент {student.name} уже есть в списке")
        else:
            self.students.append(student)
            # self.subject = self
            # self.observers.append(EmailNotifier())
            print("self.observers", self.observers)
            print("self.students", self.students)
            
            student.courses.append(self)
            self.notify()


# Интерактивный курс
class InteractiveCourse(Course):
    pass


# Курс в записи
class RecordCourse(Course):
    pass


# Категория
class Category:
    # реестр?
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# порождающий паттерн Абстрактная фабрика - фабрика курсов
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


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
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')
    
    def find_student_by_id(self, id):
        for item in self.students:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет студента с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

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
        