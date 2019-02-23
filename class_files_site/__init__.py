import sys, os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db
from .views import views


# add parent path to sys paths
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, parent_path)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('class-files-site.class_files_site.config.Config')

# load production settings 
try:
    app.config.from_object('class-files-site.instance.config.ProductionSettings')
except ImportError:
    pass

app.register_blueprint(views)
db.init_app(app)