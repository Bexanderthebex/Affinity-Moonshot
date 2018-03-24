from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
import MySQLdb
import MySQLdb.cursors
db = MySQLdb.connect(user="root", passwd="VeryLongSecurePassword123#", db="affinity", cursorclass=MySQLdb.cursors.DictCursor)
from app import routes
