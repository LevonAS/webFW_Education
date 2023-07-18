# from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from os.path import join


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """
    # file_path = join(folder, template_name)
    # print("file_path: ",file_path)
    # # Открываем шаблон по имени
    # with open(file_path, encoding='utf-8') as f:
    #     # Читаем
    #     template = Template(f.read())
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    # рендерим шаблон с параметрами
    return template.render(**kwargs)
