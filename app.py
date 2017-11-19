from flask import Flask, request, flash, jsonify
from flask_marshmallow import Marshmallow
from models import db, Employees
from json import dumps

app= Flask(__name__)

POSTGRES = {
    'user':'postgres',
    'pw':'postgres',
    'db':'flaskDB',
    'host':'localhost',
    'port':'5432',
}
app.config['DEBUG']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES
app.config['SECRET_KEY'] = 'pujan'
db.init_app(app)
ma = Marshmallow(app)

class EmpSchema(ma.Schema):
    class Meta:
        #Fields to expose
        fields = ('id','name', 'gender', 'city')



emp_schema = EmpSchema()
emps_schema = EmpSchema(many = True)


@app.route('/')
def main():
    return 'Hello World'


@app.route('/api/employees', methods = ['POST'])
def create():
    if not request.form['name'] or not request.form['gender'] or not request.form['city']:
        flash('Please enter all the fields', 'error')
    else:
        employee = Employees(request.form['name'], request.form['gender'], request.form['city'])
        db.session.add(employee)
        db.session.commit()
        flash('An Employee record was successfully added')
        result = emp_schema.dump(employee)
        return jsonify(result.data)


@app.route('/api/employees', methods = ['GET'])
def query():
    employees = Employees.query.all()
    result = emps_schema.dump(employees)
    return jsonify(result.data)

@app.route("/api/employees/<id>", methods = ["GET"])
def employee_detail(id):
    employee = Employees.query.get(id)
    result = emp_schema.dump(employee)
    return jsonify(result.data)
    

@app.route('/api/employees/<id>', methods = ['PUT'])
def update(id):
    employee = Employees.query.get(id)
    name = request.form['name']
    gender = request.form['gender']
    city = request.form['city']


    employee.name = name
    employee.gender = gender
    employee.city = city

    db.session.commit()
    return emp_schema.jsonify(employee)

@app.route('/api/employees/<id>', methods = ['DELETE'])
def remove(id):
    employee = Employees.query.get(id)
    db.session.delete(employee)
    db.session.commit()

    return emp_schema.jsonify(employee)

if __name__=='__main__':
    app.run()
