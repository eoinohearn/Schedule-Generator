from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
import main
import json



app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app,db,render_as_batch=True)


taken_courses = db.Table('taken_courses',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                         db.Column('course_database_id', db.Integer, db.ForeignKey('course_database.id'), primary_key=True)
                         )



class Course_database(db.Model):
    __name__ = 'Course_database'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    credits = db.Column(db.Integer)
    preReq = db.Column(db.String(100))
    coReq = db.Column(db.String(100))

    def __repr__(self):
        return f'Course {self.name}>'
    

class User(UserMixin, db.Model):
    __name__ = 'User'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    courses = db.relationship('Course_database', secondary=taken_courses, backref = 'users')
    schedule = db.Column(db.Text)

    def __repr__(self):
        return f'<User {self.name}>'




login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = int(user_id)).first()



@app.route("/")
def hello():
    if current_user.is_authenticated:
        schedule = current_user.schedule
        name = current_user.name.capitalize()
        return render_template('base.html', schedule = schedule, name = name)
    return render_template('base.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get('sign-up-checkbox'):

            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()
 
            if user:
                flash('Email address already exists')
                return redirect(url_for('login'))

            new_user = User(name = name, email = email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('classes'))
        else:
            email = request.form.get('email')
            password = request.form.get('password')


            user = User.query.filter_by(email=email).first()

 
            if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
                return redirect(url_for('login'))

            login_user(user)
            return redirect(url_for('classes'))
    else:
        return render_template('login.html')



@app.route("/classes",methods = ['POST', 'GET'])
def classes():
    baseList = Course_database.query.order_by(Course_database.name).all()
    user = User.query.filter(User.id == current_user.id).first()
    takenClasses = []
    for course in user.courses:
        takenClasses.append(course.name)
    return render_template('classes.html', baseList = baseList, takenClasses = takenClasses)

@app.route("/addClass", methods = ['POST'])
def addClass():
    name = request.form.get('name')
    hours = request.form.get('hours')
    preReq = request.form.get('preReq')
    coReq = request.form.get('coReq')

    if not name or not hours:
        flash('Please input both a course name and its credit hours')
        return redirect(url_for('classes'))
    course = Course_database.query.filter_by(name = name).first()

    if not preReq:
        preReq = 'empty'

    if not coReq:
        coReq = 'empty'

    if course:
        flash('Class already exists')
    else:
        new_course = Course_database(name = name, credits = hours, preReq = preReq, coReq = coReq)
        db.session.add(new_course)
        db.session.commit()


    
    return redirect(url_for('classes'))
    

@app.route("/pickSchedule", methods = ['POST', 'GET'])
def pickSchedule():

    if request.method == 'POST':
        user = User.query.filter(User.id == current_user.id).first()

        if request.form['btn'] == 'To Take':
            number_of_semesters = int(request.form['semesters'])
            quantity = int(request.form['quantity'])

            List_Of_Taken_Classes = []
            for course in user.courses:
                List_Of_Taken_Classes.append(course.name)

            List_Of_Picked_Classes = request.form.getlist("courses")
            List_Of_Picked_Classes_Database = Course_database.query.filter(Course_database.name.in_(List_Of_Picked_Classes)).all()

            main.List_Of_Tables = main.createPossibleSchedules([], number_of_semesters, List_Of_Taken_Classes, List_Of_Picked_Classes_Database, quantity)


        if request.form['btn'] == 'Have Taken':
            
            for courseName in request.form.getlist("courses"):
                course = Course_database.query.filter(Course_database.name == courseName).first()
                user.courses.append(course)
            db.session.commit()
            return redirect( url_for('classes'))
        

        if request.form['btn'] == 'Clear History':
            user.courses.clear()
            db.session.commit()
            return redirect( url_for('classes'))
        

        if request.form['btn'] == 'Delete':
            for course in request.form.getlist("courses"):
                delete_course = Course_database.query.filter_by(name = course).first()
                db.session.delete(delete_course)
                db.session.commit()
            return redirect( url_for('classes'))
    
    return render_template('schedules.html', list_of_tables = main.List_Of_Tables, favSchedule = current_user.schedule)
    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/favSchedule", methods = ['POST', 'GET'])
def favSchedule():
    if request.method == 'POST':
        jsonData = request.get_json()
        user = User.query.filter(User.id == current_user.id).first()
        user.schedule = jsonData
        db.session.commit()
        return json.dumps("Everything Good")

@app.route("/editSchedule", methods=['POST','GET'])
def editSchedule():
    baseList = Course_database.query.order_by(Course_database.name).all()
    df = main.makeDataFrameHtmlTable(current_user.schedule)
    favList = main.makeListfromDataFrame(df)
    listOfObj = []
    for semester in favList:
        listOfObj.append(list(map(lambda x:Course_database.query.filter(Course_database.name == x).first(), semester)))
        

    return render_template('editSchedule.html', schedule = listOfObj, baseList = baseList)


@app.route("/validSchedule", methods=['POST','GET'])
def validSchedule():
    if request.method == 'POST':
        schedule = request.get_json()
        scheduleList = list(map(list, schedule.values()))
        takenClasses = current_user.courses
        # check pre reqs with function, if doesnt pass then return with class failed
        # check co reqs and return failed class
        # if passes both then its a valid class and return a valid message
        scheduelObjectList = []
        for semester in scheduleList:
            scheduelObjectList.append([Course_database.query.filter(Course_database.name == course).first() for course in semester])

        if not main.satisfiesPreReq(scheduelObjectList, takenClasses):
            message = 'Did not satisfy prerequisites'
        elif not main.satisfiestCourseCoreq(scheduelObjectList):
            message = 'Did not satisfy corequisites'
        else:
            message = 'Woo Hoo!'
            current_user.schedule = main.makeHTMLTable(scheduelObjectList)
            db.session.commit()


        return json.dumps(message)
    

@app.route("/addNewClassSchedule", methods=['POST', 'GET'])
def addNewClassSchedule():
    if request.method == 'POST':
        courseNames = request.get_json()
        List_New_Classes = Course_database.query.filter(Course_database.name.in_(courseNames)).all()
        List_To_Return = []

        for course in List_New_Classes:
            temp = {}
            temp["name"] = course.name
            temp["credits"] = course.credits
            temp["preReq"] = course.preReq
            temp["coReq"] = course.coReq
            List_To_Return.append(temp)


        return json.dumps(List_To_Return)



if __name__ == '__main__':
    app.run(debug=True)
