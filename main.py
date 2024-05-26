
from flask import Flask,render_template,request
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from paswd import password

app=Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/restaurants"
mongodb=PyMongo(app).db.Restaurants

mail= Mail(app)

#mail connection
app.config['MAIL_SERVER'] ='smtp.gmail.com' 
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='22cse419.shreyafadikar@giet.edu'
app.config['MAIL_PASSWORD']=password

app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True


@app.get('/')   #request data from server
def show():
    return render_template('index.html')


@app.get('/menu')
def menu():
    return render_template('menu.html')


@app.get('/about')
def about():
    return render_template('about.html')


@app.get('/contact')
def contact():
    return render_template('contact.html')

@app.post('/con')  #post request -submit data to be procesed by server
def contacts():
    fname=request.form['fname']
    lname=request.form['lname']
    email=request.form['email']
    subject=request.form['subject']
    message=request.form['message']

    mongodb.contacts.insert_one({'fanme':fname,'lname':lname,'email':email,'subject':subject,'message':message})
    print(fname,lname,email,subject,message)
    return render_template('contact.html', msg1="All quries Submited!!!")

@app.get('/book')
def book():
    return render_template('booking.html')

mail= Mail(app)
@app.post('/set')
def booking():
    firstname=request.form['firstname']
    lastname=request.form['lastname']
    email=request.form['email']
    Table_Type=request.form['Table_Type']
    if (Table_Type == "small"):
        Table_Type="small"
    elif(Table_Type == "medium"):
        Table_Type="medium"
    else:
        Table_Type="large"
     
    Guest_Number=request.form['Guest_Number']

    Placement=request.form['Placement']
    if(Placement == "outdoor"):
        Placement= "outdoor"
    elif(Placement == "indoor"):
        Placement="indoor"
    else:
        Placement="rooftop"

    date=request.form['date']
    time=request.form['time']
    note=request.form['note']

    mongodb.bookings.insert_one({'name1':firstname,'name2':lastname,'email':email,'Table_Type':Table_Type,'Guest_Number':Guest_Number,'Placement':Placement,'date':date,'time':time,'note':note})
    print(firstname,lastname,email,Table_Type,Guest_Number,date,time,note)

    msg =Message(f'Hello {firstname} ',sender='22cse419.shreyafadikar@giet.edu', recipients=[email])
    msg.body=f'''Thank you for your reservation at Cloud kitchen
    We are expecting you on {date} ,{time}.
    
    We are looking forward to your visit and hope you will have the best dining experiences with us.


    See you soon,
    from  Cloud Kitchen.'''
     
    mail.send(msg)

    return render_template('booking.html', msg="data successfully uploaded!!!")

app.run(debug=True) 