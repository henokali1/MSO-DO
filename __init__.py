from flask import Flask, render_template, redirect, url_for, session, request, logging, json
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import dbconnector as db

app = Flask(__name__)


# Get curret user info
def current_user():
    return db.get_user_by_email(session['email'].encode('utf8'))


# Register Form Class
class RegisterForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=50)])
    airport_id = StringField('Airport ID Number', [validators.Length(min=1)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    job_title = SelectField(
        u'Job Title',
        choices=[('', ''), ('department_head', 'Department Head'),
                 ('supervisor', 'Supervisor'), ('technician', 'Technician')])
    department = SelectField(
        u'Department',
        choices=[('', ''), ('COMNAV', 'COMNAV'), ('OTHER', 'OTHER')])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        airport_id = form.airport_id.data
        email = form.email.data
        job_title = form.job_title.data
        department = form.department.data
        password = sha256_crypt.encrypt(str(form.password.data))

        sql = "insert into users(first_name, last_name, airport_id, email, job_title, password, department) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        data = (first_name, last_name, airport_id, email, job_title, password,
                department)

        db.register_user(sql, data)
        #db.register_user(sql, data)

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/")
def home():
    return redirect(url_for('login'))


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']
        # Get user by email
        data = db.get_user_by_email(email)

        if len(data) > 0:
            # Get stored hash
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email

                if current_user()['department'] == 'OTHER':
                    return redirect(url_for('mso_request'))
                elif (current_user()['job_title'] == 'supervisor') or (
                        current_user()['job_title'] == 'department_head'):
                    return 'approve.html'
                else:
                    return current_user()
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'User not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()
