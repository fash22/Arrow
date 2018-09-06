# server.py

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.fields import DateField, IntegerField
from wtforms.fields import SelectField, PasswordField
from wtforms.validators import Required

from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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
    anti_histamine = IntegerField('Anti-histamine Count', validators=[Required()])
    paracetamol = IntegerField('Paracetamol Count', validators=[Required()])

    #General Information details
    sss = StringField('SSS Number', validators=[Required()])
    gsis = StringField('GSIS Number', validators=[Required()])
    discharge_case = StringField('Discharge Case', validators=[Required()])
    discharge_summary = StringField('Discharge Case', validators=[Required()])
    discharge_from = StringField('Discharge From', validators=[Required()])
    submit = SubmitField('Add Patient')

class LoginForm(Form):
    user_name = StringField('User Name', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')

class SearchForm(Form):
    query = StringField('Search Patient')
    submit = SubmitField('Search')

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
    anti_histamine = db.Column(db.Integer, nullable=True)
    paracetamol = db.Column(db.Integer, nullable=True)

    #General Info
    sss = db.Column(db.String(80), nullable=True)
    gsis = db.Column(db.String(80), nullable=True)
    discharge_case = db.Column(db.String(80), nullable=True)
    discharge_summary = db.Column(db.String(80), nullable=True)
    discharge_from = db.Column(db.String(80), nullable=True)

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
def add_patient():
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
        user.metroprolol = form.metroprolol.data
        user.anti_histamine = form.anti_histamine.data
        user.paracetamol = form.paracetamol.data
        user.sss = form.sss.data
        user.gsis = form.gsis.data
        user.discharge_summary = form.discharge_summary.data
        user.discharge_from = form.discharge_from.data
        user.discharge_case = form.discharge_case.data
        db.session.add(user)
        db.session.commit()
        rendered_template = render_template('add_patient_confirmed.html', patient=patient)
   
    return rendered_template

@app.route('/patients', methods=['GET', 'POST'])
def patients_list():
    rendered_template = None
    form = SearchForm()
    
    if request.method == 'GET':
        patients = Patient.query.all()
        rendered_template = render_template('view_patients.html', form=form, patients=patients,)
    
    if request.args.get('filterby','') == 'agedesc':
        patients = db.session.query(Patient).order_by(Patient.age.desc())
        rendered_template = render_template('view_patients.html', patients=patients, form=form)

    if request.args.get('filterby','') == 'ageasc':
        patients = db.session.query(Patient).order_by(Patient.age.asc())
        rendered_template = render_template('view_patients.html', patients=patients, form=form)

    if request.args.get('filterby','') == 'familyname':
        patients = db.session.query(Patient).order_by("Patient.family_name")
        rendered_template = render_template('view_patients.html', patients=patients, form=form)

    if request.method == 'POST':
        q = form.query.data
        print(q)
        patients = db.session.query(Patient).filter(or_(Patient.user_name == q, Patient.middle_name == q, Patient.family_name == q, Patient.first_name == q))
        rendered_template = render_template('view_patients.html', patients=patients, form=form)

    return rendered_template

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

@app.route('/')
def sample():
    return redirect('/login')

@app.route('/patients/update/<user_name>')
def update_patient(user_name):
    form = RegisterForm()
    patient = Patient.query.filter(Patient.user_name == user_name)[0]
    return render_template('update_patient.html', patient=patient, form=form)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)


