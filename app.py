from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Job, Department
from datetime import datetime
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mars_explorer_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mars_explorer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', title='Миссия Колонизация Марса')


@app.route('/users', methods=['GET', 'POST'])
def users_page():
    users = User.query.all()

    if request.method == 'POST':
        if 'delete_id' in request.form:
            try:
                user_id = int(request.form['delete_id'])
                user = User.query.get(user_id)

                if user:
                    jobs_count = Job.query.filter_by(team_leader=user_id).count()
                    if jobs_count > 0:
                        flash(f'Нельзя удалить пользователя: у него {jobs_count} связанных работ!', 'danger')
                    else:
                        db.session.delete(user)
                        db.session.commit()
                        flash('Пользователь успешно удален!', 'success')
                else:
                    flash('Пользователь не найден!', 'danger')

            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при удалении пользователя: {str(e)}', 'danger')

        else:
            try:
                password = request.form['password']
                confirm_password = request.form['confirm_password']

                if password != confirm_password:
                    flash('Пароли не совпадают!', 'danger')
                    return redirect(url_for('users_page'))

                hashed_password = generate_password_hash(password)

                user = User(
                    surname=request.form['surname'],
                    name=request.form['name'],
                    age=int(request.form['age']) if request.form['age'] else None,
                    position=request.form['position'],
                    speciality=request.form['speciality'],
                    address=request.form['address'],
                    email=request.form['email'],
                    hashed_password=hashed_password,
                    modified_date=datetime.utcnow()
                )

                db.session.add(user)
                db.session.commit()
                flash('Пользователь успешно зарегистрирован!', 'success')

            except Exception as e:
                db.session.rollback()
                if 'UNIQUE constraint failed' in str(e):
                    flash('Пользователь с таким email уже существует!', 'danger')
                else:
                    flash(f'Ошибка при регистрации пользователя: {str(e)}', 'danger')

        return redirect(url_for('users_page'))

    return render_template('users.html', title='Пользователи', users=users)


@app.route('/jobs', methods=['GET', 'POST'])
def jobs_page():
    users = User.query.all()
    jobs = Job.query.all()

    if request.method == 'POST':
        if 'delete_id' in request.form:
            try:
                job_id = int(request.form['delete_id'])
                job = Job.query.get(job_id)

                if job:
                    db.session.delete(job)
                    db.session.commit()
                    flash('Работа успешно удалена!', 'success')
                else:
                    flash('Работа не найдена!', 'danger')

            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при удалении работы: {str(e)}', 'danger')

        else:
            try:
                start_date_str = request.form.get('start_date')
                start_date = datetime.utcnow()
                if start_date_str:
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

                end_date_str = request.form.get('end_date')
                end_date = None
                if end_date_str:
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

                job = Job(
                    team_leader=int(request.form['team_leader']),
                    job=request.form['job'],
                    work_size=int(request.form['work_size']) if request.form['work_size'] else None,
                    collaborators=request.form['collaborators'],
                    start_date=start_date,
                    end_date=end_date,
                    is_finished=request.form.get('is_finished') == 'on'
                )

                db.session.add(job)
                db.session.commit()
                flash('Работа успешно добавлена!', 'success')

            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при добавлении работы: {str(e)}', 'danger')

        return redirect(url_for('jobs_page'))

    return render_template('jobs.html', title='Работы', jobs=jobs, users=users)


@app.route('/departments', methods=['GET', 'POST'])
def departments_page():
    users = User.query.all()
    departments = Department.query.all()

    if request.method == 'POST':
        if 'delete_id' in request.form:
            try:
                dept_id = int(request.form['delete_id'])
                department = Department.query.get(dept_id)

                if department:
                    db.session.delete(department)
                    db.session.commit()
                    flash('Отдел успешно удален!', 'success')
                else:
                    flash('Отдел не найден!', 'danger')

            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при удалении отдела: {str(e)}', 'danger')

        else:
            try:
                department = Department(
                    title=request.form['title'],
                    chief=int(request.form['chief']),
                    members=request.form['members'],
                    email=request.form['email']
                )

                db.session.add(department)
                db.session.commit()
                flash('Отдел успешно добавлен!', 'success')

            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при добавлении отдела: {str(e)}', 'danger')

        return redirect(url_for('departments_page'))

    return render_template('departments.html', title='Отделы', departments=departments, users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных mars_explorer.db создана!")

    os.makedirs('static/css', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    app.run(host='127.0.0.1', port=8080, debug=True)
