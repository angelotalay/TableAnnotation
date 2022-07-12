from flask import Flask
from flask import render_template
from flask import request
import os
import tables

app = Flask(__name__)
UPLOAD_FOLDER = './json_files'


@app.route('/', methods=['GET', 'POST'])
def index_upload():
    return render_template('index.html')


@app.route('/table-display/<int:table_number>', methods=['POST'])
def render_table(table_number):
    # Get and save uploaded files from the user
    file_request = request.files['file']
    file_request.save(os.path.join(UPLOAD_FOLDER, file_request.filename))

    # Obtain relevant table data to display on the page
    table = tables.ObtainTables(f'{UPLOAD_FOLDER}/{file_request.filename}')
    table.load_json()
    table_ids, table_titles, table_captions = table.table_summary()
    table.get_table_data(table_number)
    headings = table.headers
    rows = table.get_rows()

    return render_template('render_table.html', zip=zip, range=range, len=len, table_ids=table_ids,
                           table_titles=table_titles, table_captions=table_captions, headings=headings, table_rows =rows.items(), type=type, int=int, str=str)


if __name__ == "__main__":
    app.run(debug=True)
    app.config['upload_files'] = UPLOAD_FOLDER