from flask import Flask
from flask_executor import Executor
from pymongo import MongoClient
import os

app = Flask(__name__)
executor = Executor(app)

flask_env = os.getenv('FLASK_ENV')

# MongoDB Configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI') if flask_env == 'test' else os.getenv('MONGO_URI_TEST')

app.config['OPENWEATHER_BASE_URL'] = os.getenv('OPENWEATHER_BASE_URL')

client = MongoClient(app.config['MONGO_URI'])
db = client['weather_db']
app.cities_collection = db['cities']
app.weather_collection = db['weather_data']



# Retrieving the API key from environment variables
app.config['API_KEY'] = os.getenv('OPENWEATHER_API_KEY')

# Import routes after the app configuration
from app import routes
