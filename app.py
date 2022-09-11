import flask_migrate
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import Column, Integer, String
from flask_migrate import Migrate, upgrade
import os

database_user = os.environ.get('DB_USER', 'postgres')
database_pass = os.environ.get('DB_PASSWORD', 'postgres')
database_name = os.environ.get('DB_NAME', 'postgres')
database_host = os.environ.get('DB_HOST', 'localhost')
database_port = os.environ.get('DB_PORT', '2002')
database_engine = os.environ.get('DB_ENGINE', 'SQLITE')

if database_engine == 'SQLITE':
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_URI = 'sqlite:///'+os.path.join(basedir, 'db.sqlite3')
elif database_engine == 'POSTGRES':
    database_URI = 'postgresql+psycopg2://' + database_user + ':' + database_pass + '@' + database_host + ':' + database_port + '/' + database_name
else:
    raise ValueError('Unknown DB_ENGINE Specified')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class employee(db.Model):
   __tablename__ = 'employeesinfo'
   id = db.Column(db.Integer, primary_key=True)
   firstname = db.Column(db.String(100), nullable=False)
   lastname = db.Column(db.String(100), nullable=False)
   gender = db.Column(db.String(50), nullable=False)

   def __repr__(self):
     return f"{self.firstname} - {self.lastname} - {self.gender}"


@app.route('/')
def index():
    return 'hello !!'


@app.route('/employees')
def get_employees():
    employees = employee.query.all()

    emp_list = []
    for emp in employees:
            emp_data = {'id': emp.id, 'firstname':emp.firstname, 'lastname':emp.lastname, 'gender':emp.gender}
            emp_list.append(emp_data)

    return {"employees":emp_list}


@app.route('/employees/<id>')
def get_employee(id):
    empl = employee.query.get_or_404(id)
    return jsonify({"FirstName": empl.firstname, "LastName": empl.lastname, "Gender": empl.gender})


@app.route('/employees',methods=['POST'])
def AddEmployee():
    if request.is_json:
        empl = employee(firstname=request.json['firstname'], lastname=request.json['lastname'], gender=request.json['gender'])
        db.session.add(empl)
        db.session.commit()
        return {'id': empl.id}
    else:
        return "{'error':'Request must be JSON'}"


@app.route('/employees/<id>',methods=['PUT'])
def UpdateEmployee(id):
     if request.is_json:
        empl = employee.query.get(id)
        if empl is None:
                return {'error': 'not found'}
        else:
            empl.firstname = request.json['firstname']
            empl.lasttname = request.json['lastname']
            empl.gender = request.json['gender']
            db.session.commit()
            return 'Updated'
     else:
        return {'error':'Request must be JSON'}


@app.route('/employees/<id>',methods=['DELETE'])
def DeleteEmployee(id):
    if request.is_json:
        empl = employee.query.get(id)
        if empl is None:
                return {'error':'not found'}
        else:
            db.session.delete(empl)
            db.session.commit() 
            return f'{id} is deleted'
    else:
        return {'error':'Request must be JSON'}


if __name__ == '__main__':
   # db.create_all()
   app.run(host='0.0.0.0', port=5000)
