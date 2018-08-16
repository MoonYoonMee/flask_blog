# -*- coding: UTF-8 -*-
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#其实就是返回当前路径

class Config(object):
    SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'
    #为了防止csrf攻击
    #格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式,这里是用py2，所以mysql+mysqldb
    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123456@localhost:3306/flaskblog'
    #?charset=utf8'
    #如果你不打算使用mysql，使用这个连接sqlite也可以
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
