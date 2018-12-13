# 声明所有的实体类
# 导入db 以便在实体类中使用

from . import db
from . import create_app

class User(db.Model):
    __tablename__ = 'user'
    ID = db.Column(db.Integer,primary_key=True)
    loginname = db.Column(db.String(50),nullable=False)
    uname = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    url = db.Column(db.String(200))
    upwd = db.Column(db.String(30),nullable=False)
    is_author = db.Column(db.SmallInteger,default=0)

    # 定义与topic关联关系和反向引用
    topics = db.relationship('Topic',backref='user',lazy='dynamic')
    # 定义与user和topic多对多关联关系和反向引用
    vokes_topics = db.relationship('Topic',secondary='voke',lazy='dynamic',
                                   backref=db.backref('voke_users',lazy='dynamic')
                                   )
    # 定义与reply关联关系和反向引用
    replies = db.relationship('Reply', backref='user', lazy='dynamic')



class Voke(db.Model):
    __tablename__ = 'voke'
    id = db.Column(db.Integer,primary_key=True)
    # 关系 : 一(User)对多(voke)的关系
    user_id = db.Column(db.Integer,db.ForeignKey('user.ID'))
    # 关系 : 一(Topic)对多(voke)的关系
    topic_id = db.Column(db.Integer,db.ForeignKey('topic.id'))


class Reply(db.Model):
    __tablename__  = 'reply'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT, nullable=False)
    reply_time = db.Column(db.DATETIME)
    # 关系 : 一(User)对多(reply)的关系
    user_id = db.Column(db.Integer, db.ForeignKey('user.ID'))
    # 关系 : 一(Topic)对多(reply)的关系
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))


class Topic(db.Model):
    __tablename__='topic'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    pub_date = db.Column(db.DATETIME,nullable=False)
    read_num = db.Column(db.Integer)
    content =db.Column(db.TEXT,nullable=False)
    images = db.Column(db.TEXT)

    #关系 : 一(Category)对多(topic)的关系
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))

    # 关系 : 一(User)对多(topic)的关系
    user_id = db.Column(db.Integer,db.ForeignKey('user.ID'))

    # 关系 : 一(BlogType)对多(topic)的关系
    blogtype_id = db.Column(db.Integer,db.ForeignKey('blogtype.id'))

    # 定义与voke关联关系和反向引用
    vokes = db.relationship('Voke', backref='topic', lazy='dynamic')

    # 定义与reply关联关系和反向引用
    replies = db.relationship('Reply', backref='topic', lazy='dynamic')


class Category(db.Model):
    __tablename__='category'
    id = db.Column(db.Integer, primary_key=True)
    cate_name = db.Column(db.String(50),nullable=False)
    #定义与topic关联关系和反向引用
    topics = db.relationship('Topic',backref='category', lazy='dynamic')

class BlogType(db.Model):
    __tablename__ = 'blogtype'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(20),nullable=False)
    # 定义与topic关联关系和反向引用
    topics = db.relationship('Topic',backref ='blogType', lazy='dynamic')
