from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/flask'
db = SQLAlchemy(app)

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(30), unique=True, nullable=False)
    lpwd = db.Column(db.String(30), nullable=False)
    uname = db.Column(db.String(30), unique=True, nullable=False)


db.create_all()


@app.route('/01-xhr')
def xhr():
    return render_template('01-xhr.html')

@app.route('/server')
def server():
    uname = request.args.get('uname')
    return '参数值为:'+uname
@app.route('/html')
def html():
    return  render_template('homework.html')

@app.route('/homework')
def homework():
    name = request.args.get('name')
    if Login.query.filter(Login.lname == name).first():

        return '已存在'

    else:

        return '通过'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')