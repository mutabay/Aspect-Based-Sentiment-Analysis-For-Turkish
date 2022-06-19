from flask_migrate import Migrate
from sys import exit
from decouple import config

import pandas as pd
import apps.file.routes
from apps.config import config_dict
from apps import create_app, db
from apps.file.routes import FileOperations

from flask import Flask, flash, request, redirect, url_for

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

UPLOAD_FOLDER = 'uploads'

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    config_dict['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)

file = None
filename = None


class DataStore():
    file = None
    filename = None


filedata = DataStore()


@app.route('/', methods=['GET', 'POST'])
def get_file():
    f = FileOperations()
    r = f.upload_file(app)
    file = f.file
    filename = f.filename

    return r


@app.route('/prev-analyze.html', methods=['GET', 'POST'])
def prev_analyze():
    analyze_id = None
    if request.method == 'POST':
        analyze_id = request.form.get('analyze_id')
        print("Analyze id ?> ", analyze_id)

    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")

    return redirect(url_for('home_blueprint.prev_analyze', analyze_id=analyze_id))


@app.route('/prev-analyzes.html', methods=['GET', 'POST'])
def prev_analyzes():
    delete_id = None
    if request.method == 'POST':
        delete_id = request.form.get('delete_id')
    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")

    return redirect(url_for('home_blueprint.prev_analyzes', delete_id=delete_id))


Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    app.run()
