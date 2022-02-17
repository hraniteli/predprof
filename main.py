from flask import Flask, request
import service
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///C:/Users/Maxim/Desktop/ppo_it/database.db'

db = SQLAlchemy(app)

@app.route('/<sn>/<file_name>', methods=['POST'])
def main(sn, file_name):
    _file = request.get_data().decode("UTF-8")
    data = service.parse_file(_file, sn, file_name)
    service.get_grphc(date='day')
    # Передать _file
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
