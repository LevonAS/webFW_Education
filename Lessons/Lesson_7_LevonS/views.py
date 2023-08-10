from datetime import date

from leo_framework.templator import render
from patterns.structural_patterns import AppRoute, Debug
from patterns.сreational_patterns import Engine, Logger
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    ListView, CreateView, BaseSerializer
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from patterns.data_mapper_patterns import MapperRegistry

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

#
routes = {}

# контроллер - главная страница
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))

# # контроллер - Наши курсы
# @AppRoute(routes=routes, url='/products/')
# class Products:
#     @Debug(name='Products')
#     def __call__(self, request):
#         return '200 OK', render('category_list.html', objects_list=site.categories)


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



# контроллер - список категорий
@AppRoute(routes=routes, url='/category-list/')
class CategoryListView(ListView):  
    # queryset = site.students
    template_name = 'category_list.html'

    def get_context_data(self):
        context = super().get_context_data()
        # cat_all = CategoryMapper(connection).all()
        cat_all = MapperRegistry.get_current_mapper('category').all()
        for item in cat_all:
            print('Список категорий//', item.__dict__)

        context['categories'] = cat_all
        # context['students'] = site.students
        return context


# контроллер - создать категорию
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory(CreateView):
    template_name = 'create_category.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        print("// CreateCategory name : ", name)
        new_obj = site.create_category(name, category=name)
        print("// CreateCategory new_cat : ", new_obj)
        # site.categories.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


# контроллер - список курсов
@AppRoute(routes=routes, url='/courses-list/')
class CoursesListView(ListView):  
    template_name = 'course_list.html'

    def get_context_data(self):
        context = super().get_context_data()
        cat_id = self.request_id
        # courses_by_cat_id = CourseMapper(connection).course_by_category(int(cat_id))
        courses_by_cat_id = MapperRegistry.get_current_mapper('course').courses_by_category(int(cat_id))
        for item in courses_by_cat_id:
            print('Список курсов категории//', item.__dict__)
        # print('courses_by_cat_id//', courses_by_cat_id, courses_by_cat_id.__dict__)
        context['courses'] = courses_by_cat_id

        category = MapperRegistry.get_current_mapper('category').find_cat_by_id(int(cat_id))
        print('//CoursesListView-category', category, category.__dict__)
        context['category'] = category
        return context


# контроллер - создать курс
@AppRoute(routes=routes, url='/create-course/')
class CreateCourseView(CreateView):
    template_name = 'create_course.html'
    

    def get_context_data(self):
        context = super().get_context_data()
        cat_id = self.request_id
        category = MapperRegistry.get_current_mapper('category').find_cat_by_id(int(cat_id))
        print("//CreateCourseView-category", category)
        context['category'] = category
        return context

    def create_obj(self, data: dict):
        cat_id = self.request_id
        name = data['name']
        name = site.decode_value(name)
        category = None
        if cat_id != -1:
            course = site.create_course('record', name, cat_id)
            # Наблюдатели на курсе
            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)

        course.mark_new()
        UnitOfWork.get_current().commit()


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
    template_name = 'student_list.html'

    def get_context_data(self):
        context = super().get_context_data()
        student_all = MapperRegistry.get_current_mapper('student').all()
        for item in student_all:
            print('Список студентов// ', item.__dict__)

        context['students'] = student_all
        return context
    

@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        print('new_student//:', new_obj.__dict__)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/student-details/')
class StudentDetailsView(CreateView):
    template_name = 'student_details.html'

    def get_context_data(self):
        context = super().get_context_data()
        student_id = self.request_id
        self.student_by_id = \
            MapperRegistry.get_current_mapper('student').find_by_id(int(student_id))
        context['student'] = self.student_by_id

        courses_by_student = \
            MapperRegistry.get_current_mapper('course_student').courses_by_student(int(student_id))
        for item in courses_by_student:
            print('Список курсов студента// ', item.__dict__)
        context['my_courses'] = courses_by_student

        courses_all = MapperRegistry.get_current_mapper('course').all()
        context['courses'] = courses_all
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = MapperRegistry.get_current_mapper('course').course_by_name(course_name)
        
        obj = course.add_student(self.student_by_id)
        print("///StudentDetailsView-create_obj-obj: ", obj)
        check_obj = None
        check_obj = \
            MapperRegistry.get_current_mapper('course_student').presence_check(obj)
        if not check_obj:
            obj.mark_new()
            UnitOfWork.get_current().commit()
        

@AppRoute(routes=routes, url='/course-details/')
class CourseDetailsView(CreateView):
    template_name = 'course_details.html'

    def get_context_data(self):
        context = super().get_context_data()
        course_id = self.request_id
        self.course_by_id = \
            MapperRegistry.get_current_mapper('course').find_by_id(int(course_id))
        context['course'] = self.course_by_id

        students_by_course = \
            MapperRegistry.get_current_mapper('course_student').students_by_course(int(course_id))
        for item in students_by_course:
            print('Список студентов курса// ', item.__dict__)
        context['my_students'] = students_by_course

        students_all = MapperRegistry.get_current_mapper('student').all()
        context['students'] = students_all
        return context

    def create_obj(self, data: dict):
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = MapperRegistry.get_current_mapper('student').student_by_name(student_name)
        obj = self.course_by_id.add_student(student)
        print("///CourseDetailsView-create_obj-obj: ", obj)
        check_obj = None
        check_obj = \
            MapperRegistry.get_current_mapper('course_student').presence_check(obj)
        if not check_obj:
            obj.mark_new()
            UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        students_all = MapperRegistry.get_current_mapper('student').all()
        context['students'] = students_all
        courses_all = MapperRegistry.get_current_mapper('course').all()
        context['courses'] = courses_all
        return context 

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = MapperRegistry.get_current_mapper('course').course_by_name(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = MapperRegistry.get_current_mapper('student').student_by_name(student_name)
        obj = course.add_student(student)
        print("///AddStudentByCourseCreateView-create_obj-obj: ", obj)
        
        check_obj = None
        check_obj = \
            MapperRegistry.get_current_mapper('course_student').presence_check(obj)
        if not check_obj:
            obj.mark_new()
            UnitOfWork.get_current().commit()
        


# контроллер - формирование api-страницы со-списком курсов в json формате
@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()

