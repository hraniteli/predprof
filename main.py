from flask import Flask, request
import service
from io import *
import pandas as pd

app = Flask(__name__)


@app.route('/<sn>/<file_name>', methods=['POST'])
def main(sn, file_name):
    _file = request.get_data().decode("UTF-8")
    data = service.parse_file(_file, sn, file_name)
    service.get_grphc(date='day')
    # Передать _file
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
