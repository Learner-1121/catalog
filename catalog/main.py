from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base
from sqlalchemy.orm import sessionmaker  #sessionmaker is used to store data in table
from sqlalchemy import create_engine

engine = create_engine('sqlite:///iii.db')
engine = create_engine('sqlite:///iii.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()


app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='mohini1136@gmail.com'
app.config['MAIL_PASSWORD']='svsmsury@'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.secret_key = '123'

mail=Mail(app)
otp=randint(000000,999999)


@app.route("/sample")
def demo():
    return "hello bunty,how are u"

@app.route("/demo")
def d():
    return "<h1>hello bunty Demo page</h1>"

@app.route("/info/details")
def details():
    return "hello details"

@app.route("/details/<name>/<int:no>/<float:salary>")
def info(name,no,salary):
    return "hello {} and {} and {}".format(name,no,salary)

@app.route("/details/<int:no>")
def det(no):
    return "hello {}".format(no)

@app.route("/admin")
def admin():
    return "hello Admin"

@app.route("/student")
def student():
    return "hello student"

@app.route("/staff")
def staff():
    return "hello staff"

@app.route("/info/<name>")
def admin_info(name):
    if name=='admin':
        return redirect(url_for('admin'))
    elif name=='student':
        return redirect(url_for('student'))
    elif name=='staff':
        return redirect(url_for('staff'))
    else:
        return "no url"
    
    
@app.route("/data/<name>/<int:age>/<float:sal>")
def demo_html(name,age,sal):
    return render_template('sample.html',n=name,a=age,s=sal)

@app.route("/info_data")
def info_data():
    no=1
    name='bunty'
    branch='cse' 
    return render_template('sampl.html',n=no,na=name,b=branch)

data=[{'sno':1136,'name':'bunty','branch':'cse'},
      {'sno':1121,'name':'yamba','branch':'cse'},
      {'sno':1130,'name':'venny','branch':'cse'},
      {'sno':142,'name':'kukka','branch':'cse'}]
@app.route("/dummy_data")
def dummy():
    return render_template("data.html",dummy_data=data)

@app.route("/calculator/<int:no>")
def cal(no):
    return render_template("calculator.html",n=no)

#file uploading
@app.route("/file_upload", methods=['GET','POST'])
def file_upload():
    return render_template("file_upload.html")

@app.route("/success",methods=['GET','POST'])
def success():
    if request.method=='POST':
        f=request.files['file']
        f.save(f.filename)
        return render_template("success.html",f_name=f.filename)


@app.route("/email")
def email_send():
    return render_template("email.html")

@app.route("/email_verify", methods=['POST','GET'])
def verify_email():
        email=request.form['email']
        msg=Message("One Time Password",sender="mohini1136@gmail.com",recipients=[email])
        msg.body=str(otp)
        mail.send(msg)
        return render_template("v_email.html")

@app.route("/email_success",methods=['POST','GET'])
def success_email():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        return render_template("email_success.html")
    return "In valid otp"

#DB
@app.route("/show")
def showData():
    register=session.query(Register).all()
    return render_template('show.html',reg=register)



@app.route("/form",methods=['POST','GET'])
def showform():
    if request.method=='POST':
        newData=Register(name=request.form['name'],
                         surname=request.form['surname'],
                         mobile=request.form['mobile'],
                         email=request.form['email'],
                         branch=request.form['branch'],
                         role=request.form['role'])
        session.add(newData)
        session.commit()
        flash("New Data Added...")
        return redirect(url_for('showData'))
    else:
        return render_template('form.html')


@app.route("/web")
def web_main():
    return render_template("main.html")

@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
    editedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        editedData.name=request.form['name']
        editedData.surname=request.form['surname']
        editedData.mobile=request.form['mobile']
        editedData.email=request.form['email']
        editedData.branch=request.form['branch']
        editedData.role=request.form['role']
        
        session.add(editedData)
        session.commit()
        flash(editedData.name+" account updated")
        return redirect(url_for('showData'))
    else:
        return render_template("edit.html",register=editedData)

@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deleteData(register_id):
    deletedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        delName = deletedData.name
        print(delName)
        session.delete(deletedData)
        session.commit()
        flash("deleted account of "+delName)
        return redirect(url_for('showData'))
    else:
        return render_template("delete.html",register=deletedData)

if __name__=='__main__':
    app.run(debug=True)
    






