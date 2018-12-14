#只处理与main业务相关的路由和视图
import datetime
import os

from flask import render_template, request, redirect, session, make_response

from . import main
from .. import db
from ..models import *

@main.route('/')
def main_index():
    categories = Category.query.all()
    topics = Topic.query.limit(5).all()
    topic = Topic.query.all()

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
        #登录的身份验证
        if 'uid' in session and 'loginname' in session:
            #有登录用户
            user = User.query.filter_by(ID=session.get('uid')).first()
            if user.is_author == 1:

                blog_type = BlogType.query.all()
                categories = Category.query.all()

                return render_template('release.html', params=locals())
            else:
                msg = '<script>alert("您没权限发表博客");location.href="/"</script>'
                return msg

        else:
            return redirect('/login')

    else:
        #增加博客到数据库中
        topic = Topic()
        #为title赋值
        topic.title = request.form['author']
        #为blogtype_id赋值
        topic.blogtype_id = request.form['list']
        #为category_id赋值
        topic.category_id = request.form['category']
        #为content赋值
        topic.content = request.form['content']
        #为pub_date赋值
        topic.pub_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 为user_id赋值
        topic.user_id = session.get('uid')
        #选择性为image赋值
        if request.files:
            #说明有图片上传,将图片上传至服务器,并将图片名称赋值给topic.images
            #1.从request中获取上传的图片
            file = request.files['pic']
            #2.处理文件名称(当前时间.后缀名)
            ftime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S%f')
            ext = file.filename.split('.')[1]
            filename = ftime+'.'+ext
            #3.为topic.images赋值
            topic.images = 'images/'+filename
            #4.为文件保存到服务器的指定路径上
            basedir = os.path.dirname(os.path.dirname(__file__))
            print(basedir)
            upload_path = os.path.join(basedir,'static/images',filename)
            print(upload_path)
            file.save(upload_path)
        #将topic插入进数据库
        db.session.add(topic)
        msg = '<script>alert("提交成功");location.href="/"</script>'
        return msg

@main.route('/info',methods=['GET','POST'])
def info():
    if request.method == 'GET':

        topic_id = request.args.get('topic_id')
        topic =Topic.query.filter_by(id=topic_id).first()
        #更新阅读量
        if topic.read_num == None:
            topic.read_num = 1
        else:
            topic.read_num = topic.read_num +1
        db.session.add(topic)

        #查找上一篇和下一篇
        #上一篇: 查询topic_id 比当前topic_id值小的最后一条
        prevTopic=Topic.query.filter(Topic.id<topic_id).order_by('id desc').first()
        #下一篇: 查询topic_id 比当前topic_id值大的第一条
        nextTopic=Topic.query.filter(Topic.id>topic_id).first()

        return render_template('info.html',params=locals())

