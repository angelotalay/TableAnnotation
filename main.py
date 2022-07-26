import os
from annotation_relations import Annotations, AnnotationSummary

from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import tables

app = Flask(__name__)
UPLOAD_FOLDER = './json_files'
ALLOWED_EXTENSIONS = {'json'}  # Allowed extensions not fully implemented yet
app.secret_key = 'Angelo'
app.config['upload_files'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def handle_upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['upload_files'], filename))
            return redirect(url_for('render_table', file_name=filename, table_number=0))
    return 'UPLOAD'


@app.route('/table-display/<file_name>/<int:table_number>')
def render_table(table_number, file_name):
    # Get uploaded file from the user
    file_path = os.path.join(app.config['upload_files'], file_name)
    table = tables.ObtainTables(file_path)

    # Obtain relevant table data to display on the page
    table = tables.ObtainTables(file_path)
    table.load_json()
    table_ids, table_titles, table_captions = table.table_summary()
    all_tables = table.all_table_information()

    # Get the annotations to display on the page/sidebar
    annotation_summary = AnnotationSummary(table.json)


    return render_template('render_table.html', zip=zip, range=range, len=len, table_ids=table_ids,
                           table_titles=table_titles, table_captions=table_captions, headings=table.headers, type=type,
                           int=int, str=str, dict=dict, list=list,
                           unpack=tables.unpack_annotation, file_name=file_name, tables=all_tables,
                           AnnotationsClass=Annotations, annotation_summary=annotation_summary)


if __name__ == "__main__":
    app.run(debug=True)
