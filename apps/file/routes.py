import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'csv'}
UPLOAD_FOLDER = 'uploads'


class FileOperations:
    def __init__(self):
        self.file = None
        self.filename = None

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_file(self, app):
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        if request.method == 'POST':
            # check if the post request has the file part
            if 'fileUpload' not in request.files:
                flash('No file part')
                return redirect(request.url)
            self.file = request.files['fileUpload']

            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if self.file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if self.file and self.allowed_file(self.file.filename):
                self.filename = secure_filename(self.file.filename)
                self.file.save(os.path.join(app.config['UPLOAD_FOLDER'], self.filename))
                return redirect(url_for('home_blueprint.analyze', file=self.file, filename=self.filename))

        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name=file>
              <input type=submit value=Upload>
            </form>
            '''
