import connexion
import os
from gevent.pywsgi import WSGIServer

app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yml')

if __name__ == '__main__':
	app_host = os.environ['APP_HOST'] if 'APP_HOST' in os.environ else '0.0.0.0'
	app_port = int(os.environ['APP_PORT']) if 'APP_PORT' in os.environ else 5000

	print(f"Using host: {app_host}, port: {app_port}")

	http_server = WSGIServer((app_host, app_port), app)
	http_server.serve_forever()
else:
	app = app.app
