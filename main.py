from flask import Flask, request
import service
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Maxim/Desktop/ppo_it/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/<sn>/<file_name>', methods=['POST'])
def main(sn, file_name):
    _file = request.get_data().decode("UTF-8").replace('\r', '')
    service.parse_file(_file, sn, file_name)
    # Передать _file
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
