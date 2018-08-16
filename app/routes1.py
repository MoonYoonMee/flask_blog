# -*- coding: UTF-8 -*-
from flask import render_template,flash,redirect,url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models1 import User
from flask_login import logout_user,login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm,EditProfileForm
from datetime import datetime

@app.route('/')
@app.route('/index')
#@login_required
#这样，必须登录后才能访问首页了,会自动跳转至登录页
def index():
    user = {'username':'duke'}
    posts = [
        {
            'author':{'username':'刘'},
            'body':'这是模板模块中的循环例子～1'
        },
        {
            'author': {'username': '忠强'},
            'body': '这是模板模块中的循环例子～2'
        }
    ]
    return render_template('index.html',title='我的',user=user,posts=posts)



@app.route('/login',methods=['GET','POST'])
def login():
    #判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #这是一个表单实例
    form = LoginForm()
    #验证表格中的数据格式是否正确
    if form.validate_on_submit():
        #根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        user = User.query.filter_by(username=form.username.data).first()
        #判断用户不存在或者密码不正确
        if user is None or not user.check_password(form.password.data):
            #如果用户不存在或者密码不正确就会闪现这条信息，当然在页面上要设置
            flash('无效的用户名或密码')
            #然后重定向到登录页面
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        #此时的next_page记录的是跳转至登录页面时的地址
        next_page = request.args.get('next')
        #如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '': #服务器位置（也有可能是用户信息）
            next_page = url_for('index')
        #综上，登录后要么重定向至跳转前的页面，要么跳转至首页
        return redirect(next_page)
        #这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        # login_user(user,remember=form.remember_me.data)
        # return redirect(url_for('index'))
    return render_template('login.html',title='登录',form=form)
    #     #闪现的信息会出现在页面，当然在页面上要设置
    #     flash('用户登录的名户名是:{} , 是否记住我:{}'.format(
    #         form.username.data,form.remember_me.data))
    #     #重定向至首页
    #     return redirect('/index')
    # #首次登录/数据格式错误都会是在登录界面
    # return render_template('login.html',title='登录',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user,'body':'测试Post #1号'},
        {'author':user,'body':'测试Post #2号'}
    ]

    return render_template('user.html',user=user,posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow() #now是本读时间，utnow是世界时间
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('你的提交已变更.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='个人资料编辑',form=form)