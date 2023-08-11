from jsonpickle import dumps, loads
from leo_framework.templator import render


# поведенческий паттерн - наблюдатель
# Курс
class Observer:

    def update(self, subject):
        pass

# объект наблюдения
class Subject:

    def __init__(self):
        # наблюдатели
        self.observers = []
        self.subject = None

    def attach(self, observer):      
        self.observers.append(observer)

    def detach(self, observer):       
        self.observers.remove(observer)

    # уведомление всех наблюдателей
    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):

    def update(self, subject):
        print(f"notifier SMS-> К курсу {subject.name} присоединился {subject.students[-1].name}")


class EmailNotifier(Observer):

    def update(self, subject):
        print(f"notifier EMAIL-> К курсу {subject.name} присоединился {subject.students[-1].name}")


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


# поведенческий паттерн - Шаблонный метод
class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name
    
    @staticmethod
    def get_request_id(request):
        return request['request_params']['id']

    # осуществляет рендеринг шаблона с передачей в него контекста
    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        print("\n//TemplateView request: ", request , "\n")
        # print("len", len(request['request_params']))

        if (len(request['request_params']) != 0):
            self.request_id = self.get_request_id(request)
            # print("\nrequest_id_1", self.request_id)
            
        return self.render_template_with_context()


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


# поведенческий паттерн - Стратегия
class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self):
        self.file_name = 'log.log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')

