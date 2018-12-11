from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/flask'

db = SQLAlchemy(app)

class Province(db.Model):
      __tablename__ = 'province'
      id = db.Column(db.Integer,primary_key=True)
      pname = db.Column(db.String(30))
      cities = db.relationship('City',backref='province',lazy='dynamic')

      def to_dict(self):
          dic = {
          "id":self.id,
          "pname":self.pname
          }
          return dic


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(30))
    pid = db.Column(db.Integer,db.ForeignKey('province.id'))

    def to_dict(self):
        dic = {
            'id':self.id,
            'cname':self.cname,
            'pid':self.pid
        }
        return dic

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer,primary_key=True)
    lname = db.Column(db.String(30))
    lpwd = db.Column(db.String(30))
    uname = db.Column(db.String(30))

    def to_dict(self):
        dic = {
            'id':self.id,
            'lname':self.lname,
            'lpwd':self.lpwd,
            'uname':self.uname
        }
        return dic

db.create_all()

@app.route('/01-test')
def test():
    return render_template('01-province.html')

@app.route('/01-server')
def server01():
    province = Province.query.all()
    list = []
    for i in province:
        list.append(i.to_dict())
    return json.dumps(list)

@app.route('/01-city')
def city():
    pid = request.args.get('pid')
    cities = City.query.filter_by(pid=pid).all()
    list = []
    for c in cities:
        list.append(c.to_dict())
    return json.dumps(list)


@app.route('/02-jq-load',methods=['POST','GET'])
def jq_load():
    if request.method == 'GET':
        uname = request.args['uname']
        uage = request.args['uage']
    else:
        uname = request.form['uname']
        uage = request.form['uage']

    return ('name:%s age:%s'%(uname,uage))



@app.route('/03-jq-get')
def jq_get():
    dict = {
        "uname":'万万没想到',
        'uage':20
    }
    return json.dumps(dict)

@app.route('/04-jq-post',methods=['POST'])
def jq_post():
    uname = request.form['uname']
    ugender = request.form['ugender']
    return('接收到的名字:%s,接收到的性别%s'%(uname,ugender))

@app.route('/05-login')
def login():
    uname = request.args['uname']
    if Login.query.filter_by(uname=uname).first():
        dic = {
            'status': 1,
            'text':'用户名称存在'
        }

    else:
        dic = {
            'status':0,
            'text':'通过'
        }
    return json.dumps(dic)

if __name__ == '__main__':
    app.run(debug=True)