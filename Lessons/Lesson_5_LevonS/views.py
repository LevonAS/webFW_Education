from datetime import date

from leo_framework.templator import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


# контроллер - главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))

# контроллер - Наши курсы
class Products:
    def __call__(self, request):
        return '200 OK', render('products.html', objects_list=site.categories)


# контроллер "О проекте"
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))


# контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'



# контроллер - список курсов
class CoursesList:
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name, 
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('products.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        # for item in site.categories:
        #     print('Список категорий//', item.__dict__)
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


# контроллер - копировать курс
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


class StudentList:
    def __call__(self, request):
        logger.log('Список студентов')

        # for item in site.students:
        #     print('Список студентов//:', item.__dict__)
        return '200 OK', render('student_list.html',
                                objects_list=site.students)




class StudentCreate:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            new_student = site.create_student(name)
            # print('new_student//:', new_student.__dict__)
   
            site.students.append(new_student)

            return '200 OK', render('student_list.html', objects_list=site.students)
        
        else:
            students = site.students
            return '200 OK', render('create_student.html',
                                    students=students)

