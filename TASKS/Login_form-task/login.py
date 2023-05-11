from flask import Flask,render_template,redirect,request,flash,url_for,session,render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import random
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.sqlite3'
app.config['SECRET_KEY'] = "secret key"
db = SQLAlchemy(app)
class Register(db.Model):
    
    email = db.Column(db.String(50),primary_key=True)
    password =db.Column(db.String(50))

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.secret_key = "premal"
mail = Mail(app)

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=   request.form.get('email')
        password= request.form.get('psw')
        repeat_pass = request.form.get('psw-repeat')
        # print("the data is.....",email)
        # entry=""
        if password == repeat_pass:
            try:
                user = Register.query.filter_by(email=email).first()
                if user == None:
                    entry= Register(email=email,password=password)
                    db.session.add(entry)
                    db.session.commit()
                    print("entries is",entry)
                    return redirect('sign_in')
                else:
                    flash("This Email is Already registered...")
                    return redirect(url_for('login'))
            except Exception as e:
                print("entry issss",entry)
                
                    # return "already registered"
                print("error is....",e)
        else:
            # return
            print("You enter wrong pass")
            # a= "wrong pass..."
            flash("you are not successfuly logged in")
            return redirect(url_for('login'))
            


    return render_template('index.html')

@app.route('/sign_in',methods=["GET","POST"])
def sign_in():
    if request.method=="POST":
        email = request.form.get('email')
        password= request.form.get('psw')
        user = Register.query.filter_by(email=email).first()
        if user :
            if user.password==password:
                session['email'] = request.form['email']

                # print("model pass is:",password,user.password,user.email)
                return redirect(url_for('Welcome'))
            else:
                flash("Please Enter correct pass")
                return redirect(url_for('sign_in'))
                
        else:
            flash("Please Register First")
            return redirect(url_for('sign_in'))
            
    else:
      return render_template('sign_in.html')

@app.route('/home',methods=['POST','GET'])
def Welcome():
    # email = request.form.get('email')
    # print("dfsfsfffffsfsfsdfdf",email)

    if request.method=="POST":
        pass
        
    else:
        # name = request.args.get("name")
        # print("heelkrwejrenfjkenfjergjrngfnfnfknfnsfnfdsnfnkjsdnfkdsnfksdn")
        # return render_template('home.html')
        # print("in this post...............")
            # return render_template_string("""
            #     {% if session['email'] %}
            #         <h1>Welcome {{ session['email'] }}!</h1>
            #     {% else %}
            #         <h1>Welcome! Please enter your email <a href="{{ url_for('sign_in') }}">here.</a></h1>
            #     {% endif %}
            # """)
            return render_template('home.html')
    

@app.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
        
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('psw')
        new_password = request.form.get('new_psw')
        psw_password = request.form.get('psw-repeat')
        user = Register.query.filter_by(email=email).first()
        if user:

            if user.password==password:
                if new_password==psw_password:
                    user.password=new_password
                    db.session.commit()
                    return redirect('sign_in')
                else:
                    # return "please enter same password"
                    flash("Please Enter Same Password")
                    return redirect(url_for('change_pass'))

            else:
                # return "please enter valid password"    
                flash("Please Enter Valid Password")
                return redirect(url_for('change_pass'))
           
        else:
            return "user is not matched..."
    else:
        return render_template('change_pass.html')
    

@app.route('/sign_out', methods=["GET", "POST"])
def sign_out():
    del session['email']
    return redirect(url_for('sign_in'))

def __init__(self, email, password):
   self.email = email
   self.password = password


@app.route("/forgot_pass",methods=['GET','POST'])
def forgot_pass():
    otp = ""
    if request.method=="POST":  
        n = str(random.randint(100000, 999999))
        email = request.form['email']
        session['gmail']=email
        user = Register.query.filter_by(email=email).first()
        
        # print('fdkfdf+++++++++++++++++++++++++++++++++++',user)
        if user:   
            print("this is mail....",email)
            msg = Message('Hello from the other side!',
                        sender='patelbhai1610@gmail.com', recipients=[email])
            msg.body = "hey, email from Premal!!! Your otp is:- " + n
            # msg.html = render_template_string(
            #     '''<a href="{{ url_for('login') }}">here</a>''')

            # msg.html = '<a href ="http://127.0.0.1:5000/new_forgot_pass"> here </a>'
            mail.send(msg)
            # print("the opt is.....:",n)
            # a = Otp(email=email,otp=n)
            # db.session.add(a)
            # db.session.commit()
            session['n']=n
            return redirect(url_for('get_otp'))
        else:
            # return "you are not registered user..."
            return render_template('not_register.html')
    else:
     return render_template('reset.html')
    
# for using reset link in registered mail


@app.route("/reset_link", methods=['GET', 'POST'])
def reset_link():
    otp = ""
    if request.method == "POST":
        email = request.form['email']
        session['gmail'] = email
        user = Register.query.filter_by(email=email).first()
        # print('fdkfdf+++++++++++++++++++++++++++++++++++',user)
        if user:
            print("this is mail....", email)
            msg = Message('Hello from the other side!',
                          sender='patelbhai1610@gmail.com', recipients=[email])
            # msg.body = "hey, email from Premal!!! Your otp is:- " + n

            # msg.html = render_template_string(
            #     '''<a href="{{ url_for('login') }}">here</a>''')

            msg.html = '<a href ="http://127.0.0.1:5000/new_forgot_pass"> here </a>'
            mail.send(msg)
            return redirect(url_for('sign_in'))
            
            # session['n'] = n
            # return redirect(url_for('get_otp'))
        else:
            # return "you are not registered user..."
            return render_template('not_register.html')
    else:
     return render_template('reset_link.html')


@app.route("/get_otp", methods=['GET', 'POST'])
def get_otp():
    # n = request.args.get('otp')
    if request.method == "POST":
        otp = str(request.form['otp'])
        # otpa = request.form['otpa']
        print("otp is..",otp)

        otpa= session['n']
        # print("fnjkfnjfnjnfjnsjnsnrewkr", otpa)

        if otpa==otp:
        #    print(":inner if",n)
        #    return "otp matched......"
            return redirect(url_for('new_forgot_pass'))
    return render_template('mail.html')    


@app.route("/new_forgot_pass", methods=['GET', 'POST'])
def new_forgot_pass():
    if request.method=="POST":
        password = request.form.get('new_psw')
        repeat_pass = request.form.get('psw-repeat')
        if password == repeat_pass:
            user = Register.query.filter_by(email=session['gmail']).first()
            user.password = password
            db.session.commit()
            return redirect(url_for('sign_in'))
        else:
            flash("Please Enter same PAssword")
            return redirect(url_for('new_forgot_pass'))
    else:
        return render_template('new_forgot_pass.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
