from datetime import date
from views import Index, About, Contact, Products, \
    CoursesList, CreateCourse, CreateCategory, CategoryList, CopyCourse, \
    StudentList, StudentCreate


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/products/': Products(),
    '/about/': About(),
    '/contact/': Contact(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-course/': CopyCourse(),
    '/student-list/': StudentList(),
    '/student-create/': StudentCreate(),
}
