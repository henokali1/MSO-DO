
from flask import Flask, render_template, redirect, url_for, session, request, logging, json
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import dbconnector as db

app = Flask(__name__)

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
        data = (first_name, last_name, airport_id, email, job_title, password, department)        

        db.register_user(sql, data)
        #db.register_user(sql, data)

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/")
def hello():
    return render_template('login.html')

@app.route('/login')
def login():
	return render_template('login.html')

if __name__ == "__main__":
    app.run()
