# -*- coding: utf-8 -*-
from flask import Flask, request, g, render_template, redirect, url_for, session
import config
from models import db, User, API, Project
from decorators import login_required
from sqlalchemy import or_

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

''' 
@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('1question1.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>')
def detail(question_id):
    context = {
        'question': Question.query.filter(Question.id == question_id).first()
    }
    return render_template('detail.html', **context)


@app.route('/add_answer/', methods=['POST', 'GET'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    # user_id = session.get('user_id')
    # user = User.query.filter(User.id == user_id).first()
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.route('/search/')
@login_required
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),
                                          Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html', questions=questions)
'''


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

'''
@app.route('/add_api/', methods=['POST', 'GET'])
@login_required
def add_api():
    url_api = request.form.get('url_api')
    method_api = request.form.get('method_api')
    headers_api = request.form.get('headers_api')
    payload_api = request.form.get('payload_api')
    api = API(url=url_api, method=method_api, headers=headers_api, payload=payload_api)
    api.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))
'''


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
