from datetime import timedelta
from flask import Flask
from os import environ
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()

def init_app():
	app = Flask(__name__)
	CORS(app,resources={r'*':{'origins':'*','supports_credentials':True}})
	
	load_dotenv()
	app.config['DEBUG'] = eval(environ["DEBUG_MODE"]) # Debug mode for flask app
	app.config['SQLALCHEMY_DATABASE_URI'] = environ["MYSQL_URL"] # connection string for postgres sql database
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # set it to False to disable tracking and use less memory
	app.config['JWT_SECRET_KEY'] = environ["JWT_SECRET"] # secret key for JWT
	app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
	app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

	print('\tFlask App configurations loaded...')

	db.init_app(app)
	print('\tDatabase initialised...')
	jwt.init_app(app)
	print('\tJWT initialised...')

	# first register the blue prints which
	# will initialise the db models like
	# user,post etc.
	from src.user import user_blueprint
	from src.post import post_blueprint
	for blueprint in [user_blueprint,post_blueprint]:
		print('\troutes for '+str(blueprint)+' loaded...')
		app.register_blueprint(blueprint)

	# now create tables for the initialised
	# db models
	with app.app_context():
		db.create_all()
	print('\tDatabase tables created...')
	print('\tFlask App created successfully...')
	return app