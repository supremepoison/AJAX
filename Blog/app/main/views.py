#只处理与main业务相关的路由和视图
from flask import render_template, request, redirect, session, make_response

from . import main
from .. import db
from ..models import *

@main.route('/')
def main_index():
    categories = Category.query.all()
    topics = Topic.query.limit(5).all()
    if 'uid' in session and 'loginname' in session:
        user = User.query.filter_by(ID=session.get('uid')).first()
    return render_template('index.html', params=locals())



@main.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        #将login.html内容构建成响应对象
        resp = make_response(render_template('login.html'))
        #获取请求源路径
        url = request.headers.get('Referer','/')

        resp.set_cookie('url',url)

        return  resp
    else:
        username = request.form['username']
        pwd = request.form['password']
        url = request.cookies['url']

        users = User.query.filter(username == User.loginname, pwd == User.upwd).first()
        if users:
            #登录成功
            session['loginname'] = users.loginname
            session['uid'] = users.ID
            resp=redirect(url)
            resp.delete_cookie('url')

            return resp
        else:
            return render_template('login.html',errMsg='用户名或密码不正确')

@main.route('/logout')
def logout():
    if 'uid' in session and 'loginname' in session:
        del session['uid']
        del session['loginname']
    url = request.headers.get('Referer','/')
    return redirect(url)

@main.route('/release',methods=['POST','GET'])
def release():
    if request.method == 'GET':
        blog_type = BlogType.query.all()

        return render_template('release.html',params=locals())
    else:
        images = request.files['']

