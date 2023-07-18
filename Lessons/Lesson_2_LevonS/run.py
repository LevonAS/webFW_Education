from wsgiref.simple_server import make_server
import os, sys

from leo_framework.main import Framework
from urls import routes, fronts


project_directory = os.getcwd()
# sys.path.append(project_directory)
print("project_directory: ", project_directory)
print("sys.path: ", sys.path)

application = Framework(routes, fronts)

with make_server(host="0.0.0.0", port=8000, app=application) as httpd:
    print("Запуск на порту 8000...")
    httpd.serve_forever()
