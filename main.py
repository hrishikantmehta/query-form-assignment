from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

import os

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/webdev_assignment'
app.config['SECRET_KEY']='hrishikant'
db = SQLAlchemy(app)
mail=Mail(app)

class Query(db.Model):
    '''
    id, name, email, subject, message
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)

@app.route('/', methods = ['GET','POST'])
def index():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        entry = Query(name=name, email=email, subject=subject, message=message)
        db.session.add(entry)
        db.session.commit()

        msg = Message('New Query Submitted :' + subject, sender = email, recipients = ['hrishikantmehta1@gmail.com'])
        msg.body = "Name : "+name+"\nEmail : "+email+"\nMessage : "+message
        mail.send(msg)

        session['submitted'] = "Yes"
        return redirect(url_for("index"))

    if 'submitted' in session.keys():
        del session['submitted']
        flash("Your query has been submitted")
        return render_template('index.html')
    else:
        return render_template('index.html')
    