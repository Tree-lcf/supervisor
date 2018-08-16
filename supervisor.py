# -*- coding: utf-8 -*-
from flask import Flask, request, g, render_template, redirect, url_for, session
import config
from models import db, User, API, Project
from decorators import login_required
from sqlalchemy import or_
import requests

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'projects': Project.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return "填写错误"


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        pw1 = request.form.get('password1')
        pw2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return "该手机号已注册"
        else:
            if pw1 != pw2:
                return "密码两次设定不等"
            else:
                user = User(telephone=telephone, username=username, password=pw1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))


@app.route('/test/<api_id>')
@login_required
def test(api_id):
    pass
    '''
    api = API.query.filter(API.id == api_id).first()
    url = api.url
    method = api.method
    headers = api.headers
    payload = api.payload
    res = requests()
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('index'))'''


@app.route('/search/')
@login_required
def search():
    q = request.args.get('q')
    projects = Project.query.filter(Project.name.contains(q)).order_by('-create_time')
    return render_template('index.html', projects=projects)


@app.route('/project/', methods=['GET', 'POST'])
@login_required
def project():
    if request.method == 'GET':
        return render_template('project.html')
    else:
        project_name = request.form.get('project_name')
        project = Project(name=project_name)
        project.author = g.user
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<project_name>')
@login_required
def detail(project_name):
    context = {
        'project': Project.query.filter(Project.name == project_name).first()
    }
    return render_template('detail.html', **context)


@app.route('/add_api/', methods=['POST', 'GET'])
@login_required
def add_api():
    module_api = request.form.get('module')
    url_api = request.form.get('url')
    method_api = request.form.get('method')
    headers_api = request.form.get('headers')
    payload_api = request.form.get('payload')
    project_name = request.form.get('project_name')
    api = API(module=module_api, url=url_api, method=method_api, headers=headers_api, payload=payload_api)
    api.author = g.user
    project = Project.query.filter(Project.name == project_name).first()
    api.project = project
    db.session.add(api)
    db.session.commit()
    return redirect(url_for('detail', project_name=project_name))


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


if __name__ == '__main__':
    app.run()
