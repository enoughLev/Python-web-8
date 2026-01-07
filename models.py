from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    position = db.Column(db.String(100))
    speciality = db.Column(db.String(100))
    address = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(200), nullable=False)
    modified_date = db.Column(db.DateTime, default=datetime.utcnow)

    jobs_led = db.relationship('Job', backref='leader', foreign_keys='Job.team_leader', lazy=True)
    departments_led = db.relationship('Department', backref='chief_user', foreign_keys='Department.chief', lazy=True)


    def __repr__(self):
        return f'<Colonist> {self.id} {self.surname} {self.name}'


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_leader = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job = db.Column(db.String(500), nullable=False)
    work_size = db.Column(db.Integer)
    collaborators = db.Column(db.String(500))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_finished = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return f'<Job> {self.job}'


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    chief = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    members = db.Column(db.String(500))
    email = db.Column(db.String(100))


    def __repr__(self):
        return f'<Department> {self.title}'
