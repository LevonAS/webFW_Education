from datetime import date

from leo_framework.templator import render
from patterns.structural_patterns import AppRoute, Debug
from patterns.сreational_patterns import Engine, Logger
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    ListView, CreateView, BaseSerializer

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

#
routes = {}

# контроллер - главная страница
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))

# контроллер - Наши курсы
@AppRoute(routes=routes, url='/products/')
class Products:
    @Debug(name='Products')
    def __call__(self, request):
        return '200 OK', render('products.html', objects_list=site.categories)


# контроллер "О проекте"
@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')

# 
@AppRoute(routes=routes, url='/contact/')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))


# контроллер 404
class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'



# контроллер - список курсов
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            for item in category.courses:
                print('Список курсов//', item.__dict__)
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name, 
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
@AppRoute(routes=routes, url='/create-course/')
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
                # Наблюдатели на курсе
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
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
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост

            data = request['data']
            print("CreateCategory data// ", data)

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')
            print("CreateCategory category_id// ", category_id)

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
@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        for item in site.categories:
            print('Список категорий//', item.__dict__)
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


# контроллер - копировать курс
@AppRoute(routes=routes, url='/copy-course/')
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

@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    for item in site.students:
        print('Список студентов//:', item.__dict__)
    
    queryset = site.students
    template_name = 'student_list.html'


# @AppRoute(routes=routes, url='/student-details/')
# class StudentListDetailsView():
#     def __call__(self, request):
#         logger.log('Список курсов')
#         try:
#             student = site.find_student_by_id(
#                 int(request['request_params']['id']))

#             print('StudentListDetailsView// ', student.__dict__)
#             return '200 OK', render('student_details.html',
#                                     objects_list=student.courses,
#                                     name=student.name, 
#                                     id=student.id)
#         except KeyError:
#             return '200 OK', 'Student not yet added'



@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        print('new_student//:', new_obj.__dict__)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/student-details/')
class StudentDetailsView(CreateView):
    template_name = 'student_details.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        # print("\nrequest_id_2", self.request_id)
        try:
            self.student = site.find_student_by_id(
                int(self.request_id))

            # print('StudentDetailsView// ', self.student.__dict__)
            context['student'] = self.student
        except KeyError:
            return '200 OK', 'Student not yet added'
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        course.add_student(self.student)
        

@AppRoute(routes=routes, url='/course-details/')
class CourseDetailsView(CreateView):
    template_name = 'course_details.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['students'] = site.students
        # print("\nrequest_id_2", self.request_id)
        try:
            self.course = site.find_course_by_id(
                int(self.request_id))
            # print('CourseDetailsView// ', self.course.__dict__)
            context['course'] = self.course
        except KeyError:
            return '200 OK', 'Course not yet added'
        return context

    def create_obj(self, data: dict):
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        self.course.add_student(student)


# контроллер - формирование api-страницы со-списком курсов в json формате
@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()

# # контроллер - список студентов
# @AppRoute(routes=routes, url='/student-list/')
# class StudentList:
#     def __call__(self, request):
#         logger.log('Список студентов')

#         # for item in site.students:
#         #     print('Список студентов//:', item.__dict__)
#         return '200 OK', render('student_list.html',
#                                 objects_list=site.students)


# # контроллер - создание студента
# @AppRoute(routes=routes, url='/student-create/')
# class StudentCreate:
#     def __call__(self, request):

#         if request['method'] == 'POST':
#             # метод пост

#             data = request['data']

#             name = data['name']
#             name = site.decode_value(name)

#             new_student = site.create_student(name)
#             # print('new_student//:', new_student.__dict__)
   
#             site.students.append(new_student)

#             return '200 OK', render('student_list.html', objects_list=site.students)
        
#         else:
#             students = site.students
#             return '200 OK', render('create_student.html',
#                                     students=students)

