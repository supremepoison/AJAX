from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/flask'

db = SQLAlchemy(app)

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

@app.route('/homework')
def homework():
    return render_template('homework.html')

@app.route('/server')
def server():
    lname = request.args.get('lname')
    if Login.query.filter_by(lname = lname).first():
        return ' 用户名已存在'
    else:
        return '通过'

@app.route('/01-post')
def post():
    return render_template('01-post.html')

@app.route('/01-server',methods=['POST'])
def server_01():
    uname = request.form['uname']
    uage = request.form['uage']
    return '传递过来uname value:%s,c传递过来的uage value: %s' %(uname,uage)

@app.route('/02-form',methods=['GET','POST'])
def form():
    if request.method == 'GET':
        return  render_template('02-form.html')
    else:
        uname = request.form['uname']
        uage = request.form['uage']
        return '传递过来uname value:%s,c传递过来的uage value: %s' % (uname, uage)
@app.route('/03-login')
def login():
    return  render_template('03-getlogin.html')

@app.route('/03-server')
def server03():
    logins = Login.query.all()
    strs = ''
    for login in logins:
        strs += str(login.id)
        strs += login.lname
        strs += login.uname
    return strs

@app.route('/04-json')
def Json():
    return render_template('04-json.html')

@app.route('/04-server')
def server04():
    # list = ["王老刘","Rap王","隔壁老王"]
    # 将list 转换为 json格式的字符串
    # dic = {
    #     'name':'teacherwang',
    #     'age':23,
    #     'gender':'male'
    # }

    list = [

        {'name':'teacherwang',
         'age':23,
        'gender':'male'},

        {'name': 'wangwc',
         'age': 33,
         'gender': 'female'}
    ]

    jsonStr = json.dumps(list)
    return jsonStr

@app.route('/05-server')
def server05():
    #得到id 为1的Login的信息
    login = Login.query.filter_by(id=1).first()

    jsonStr = json.dumps(login.to_dict())
    return jsonStr

@app.route('/05-json-login')
def json_login():
    return render_template('05-json-login.html')
if __name__ == '__main__':
    app.run(debug=True)