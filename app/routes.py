from app import moment
from app.forms import AddTask, LoginForm, RegisterForm
from app import app, db
from app.models import User, ToDo
from urllib.parse import urlparse
from flask import render_template, url_for, redirect, request, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = AddTask()
    tasks = current_user.user_tasks.all()

    return render_template('index.html', title='Home', tasks=tasks, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sing In', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Done, you are registered now!')
        return redirect('login')
    return render_template('register.html', form=form, title='Register')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/delete', methods=['GET','POST'])
@login_required
def delete():
    if request.method == 'POST':  # Method verification
        name = request.form['name']
        task = ToDo.query.get(name)
        if task.creator == current_user:  # Owner verification
            db.session.delete(task)
            db.session.commit()
            return '', 200
        return '', 400
    return redirect('index')

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = AddTask()
    if request.method == 'POST':
        if form.validate_on_submit():
            task = ToDo(title=form.task.data, due_date=form.end_date.data, creator=current_user)
            db.session.add(task)
            db.session.commit()
            return jsonify(
                id=task.id,
                title=task.title,
                due_date=task.due_date,
                status=task.status
            )
        return '', 400

@app.route('/check_status', methods=['GET','POST'])
@login_required
def check_status():
    if request.method == 'POST':  # Method verification
        id = request.form['id']
        status = request.form['status']
        task = ToDo.query.get(id)
        if task.creator == current_user:  # Owner verification
            task.status = bool(int(status))
            db.session.add(task)
            db.session.commit()
            return '', 200
        return '', 400
    return redirect('index')
