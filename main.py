from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import service


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Maxim/Desktop/ppo_it/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('ppo_it_8/<sn>/<file_name>', methods=['POST'])
def main(sn, file_name):
    _file = request.get_data().decode("UTF-8").replace('\r', '')
    service.parse_file(_file, sn, file_name)
    # Передать _file
    return 'ok'


if __name__ == '__main__':
    app.run(port=8818, debug=True)
