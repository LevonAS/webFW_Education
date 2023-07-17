from wsgiref.simple_server import make_server

from leo_framework.main import Framework
from urls import routes, fronts


application = Framework(routes, fronts)

with make_server(host="0.0.0.0", port=8000, app=application) as httpd:
    print("Запуск на порту 8000...")
    httpd.serve_forever()
