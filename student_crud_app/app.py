from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

# Initialize Flask app and configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    grade = db.Column(db.String(10), nullable=False)

# Create tables within application context
with app.app_context():
    db.create_all()

# Forms
class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=120)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    grade = StringField('Grade', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('')

# Flask-Login setup
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    students = Student.query.paginate(page=page, per_page=5)
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Student(name=form.name.data, age=form.age.data, gender=form.gender.data, grade=form.grade.data)
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.age = form.age.data
        student.gender = form.gender.data
        student.grade = form.grade.data
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_student.html', form=form)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return '', 204 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect to home if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else :
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
