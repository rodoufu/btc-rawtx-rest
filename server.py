import connexion
import os

app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yml')

if __name__ == '__main__':
	app_host = os.environ['APP_HOST'] if 'APP_HOST' in os.environ else '0.0.0.0'
	app_port = int(os.environ['APP_PORT']) if 'APP_PORT' in os.environ else 5000
	app_debug = bool(os.environ['APP_DEBUG']) if 'APP_DEBUG' in os.environ else True

	print(f"Using host: {app_host}, port: {app_port}, debug: {app_debug}")

	app.run(host=app_host, port=app_port, debug=app_debug)
