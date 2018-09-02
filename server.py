# server.py

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.fields import DateField, IntegerField
from wtforms.fields import SelectField, PasswordField
from wtforms.validators import Required

from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/John Rey Faciolan/Desktop/Project Arrow/test.db'
app.config['SECRET_KEY'] = 'S#I#N#O#A#N#G#P#A#G#L#A#U#M#M#O'
db = SQLAlchemy(app)

class RegisterForm(Form):
    user_name = StringField('User Name', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    date_admitted = DateField('Date Admitted', format='%m-%d-%Y',validators=[Required()])
    first_name = StringField('First Name', validators=[Required()])
    middle_name = StringField('Middle Name', validators=[Required()])
    family_name = StringField('Family Name', validators=[Required()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[Required()])
    birth_date = DateField('Date of Birth', format='%m-%d-%Y',validators=[Required()])
    age = IntegerField('Age', validators=[Required()])
    #health related data
    bp = IntegerField('Blood Pressure', validators=[Required()])
    metroprolol = IntegerField('Metroprolol Count', validators=[Required()])
    submit = SubmitField('Add Patient')

class LoginForm(Form):
    user_name = StringField('User Name', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    date_admitted = db.Column(db.Date, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(120), nullable=False)
    family_name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    #health related data
    bp = db.Column(db.Integer, nullable=True)
    metroprolol = db.Column(db.Integer, nullable=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<Patient %r>' % self.user_name
    

@app.route('/patients/add', methods=['GET','POST'])
def index():
    form = RegisterForm()
    patient = {}
    rendered_template = None

    if request.method == 'GET':
        rendered_template = render_template('add_patient.html', form=form)

    elif request.method == 'POST':
        patient['user_name'] = form.user_name.data
        patient['first_name'] = form.first_name.data
        patient['family_name'] = form.family_name.data

        #add to database
        db.create_all()

        user = Patient()
        user.date_admitted = form.date_admitted.data
        user.user_name = form.user_name.data
        user.first_name = form.first_name.data
        user.middle_name = form.middle_name.data
        user.family_name = form.family_name.data
        user.gender = form.gender.data
        user.birth_date = form.birth_date.data
        user.age = form.age.data
        user.password = form.password.data
        user.bp = form.bp.data
        user.metroprolol = form.metroprolol.data
        db.session.add(user)
        db.session.commit()
        rendered_template = render_template('add_patient_confirmed.html', patient=patient)
   
    return rendered_template

@app.route('/patients')
def patients_list():
    patients = Patient.query.all()
    print(patients)
    return render_template('view_patients.html', patients=patients)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    rendered_template = None

    if request.method == 'GET':
        rendered_template = render_template('login.html', form=form)

    elif request.method == 'POST':
        account = Patient.query.filter(Patient.user_name == form.user_name.data)[0]
        if account.verify_password(form.password.data):
            print("Password correct")
            rendered_template = render_template('patient_page.html', account=account)
        else:
            print('Password Incorrect')
            err = "Your password is incorrect"
            rendered_template = render_template('error_message.html', err_message=err)

        print(account)
        

    return rendered_template

if __name__ == '__main__':
    #db.drop_all()
    #db.create_all()
    app.run(debug=True)


