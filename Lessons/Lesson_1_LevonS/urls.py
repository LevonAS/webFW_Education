from datetime import date
from views import Index, About, Contact, Products


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
    # '/about.html': About(),
    '/contact/': Contact(),
    # '/contact.html': Contact(),
}
