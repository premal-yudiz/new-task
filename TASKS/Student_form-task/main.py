from flask import Flask,redirect,render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
# Git test

app = Flask(__name__)
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_form.sqlite3'
    app.config['SECRET_KEY'] = "secret key"
    db = SQLAlchemy(app)
except Exception as e:
    print(e)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(50))


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))

class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    roll_num = db.Column(db.Integer, unique=True)
    sub = db.Column(db.Integer,db.ForeignKey("subject.id"))
    sub_teacher = db.Column(db.Integer, db.ForeignKey("teacher.id"))
    marks = db.Column(db.Integer)






# with app.app_context():
#     new_teacher = Teacher(teacher_name='John Smith')
#     db.session.delete(Teacher.query.get(2))
#     db.session.commit()

# with app.app_context():
#     new_teacher = Teacher(teacher_name='Abhishek')
#     db.session.add(new_teacher)
#     db.session.commit()







@app.route('/', methods=['GET', 'POST'])
def form():
    t = Teacher.query.all()
    sub=Subject.query.all()
    if request.method=="POST":

        s_name = request.form.get('name')
        roll_num = request.form.get('roll_num')
        subject = request.form.get('subject')
        teacher = request.form.get('teacher')

        s_marks = request.form.get('marks')
        
        entry = Student(name=s_name, roll_num=roll_num,
                        marks=s_marks, sub=subject, sub_teacher=teacher)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('list'))

    else:
        return render_template('main.html',tech=t,subj=sub)


@app.route('/list')
def list():
    s_list = Student.query.all()
    for s in s_list:
        s.subject = Subject.query.get(s.sub).subject
        # print("Subject: ",s.subject)
        s.sub_teacher = Teacher.query.get(s.sub_teacher).teacher_name
        # print("teacher: ", s.sub_teacher)
    
    
    return render_template("list.html",student_list=s_list)

@app.route('/update/<id>', methods=["GET","POST"])
def update(id):
    t = Teacher.query.all()
    sub = Subject.query.all()
    if request.method == "POST":

        update_data = Student.query.get(id)
        update_data.name = request.form.get("name")
        update_data.marks = request.form.get("marks")
        update_data.sub = request.form.get("subject")
        update_data.sub_teacher = request.form.get("teacher")
        db.session.commit()
        return redirect(url_for('list'))
    else:
        matched_record = Student.query.get(id)
        # print(std)
        return render_template('update.html', matched_record=matched_record, tech=t, subj=sub)

@app.route('/delete/<id>')
def delete(id):
    delete_data = Student.query.get(id)
    try:
        db.session.delete(delete_data)
        db.session.commit()
        return redirect(url_for('list'))

    except Exception as e:
        print(e)







# conn = sqlite3.connect('Teacher.db')
# cursor = conn.cursor()
# cursor.execute('''INSERT INTO Teacher(
#    teacher_name) VALUES 
#    ("premal")''')
# conn.commit()

if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()   
    app.run(debug=True)




