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

@app.route('/00-server')
def server00():
    #查询Login中所有的数据
    logins = Login.query.all()
    #再将所有的数据转换JSON格式的字符串
    list = []
    for l in logins:
        list.append(l.to_dict())
    return json.dumps(list)


if __name__ == '__main__':
    app.run(debug=True)