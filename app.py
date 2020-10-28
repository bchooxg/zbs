from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField


app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app,db)

class CreateAdminForm(FlaskForm):
    name = StringField("Whats your preferred name")
    username = StringField("Desired Username?")
    password = PasswordField('Desired Password?')
    submit = SubmitField('Submit')

class Channel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Task %r>'% self.id

class Admin(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50))


@app.route('/', methods=['POST','GET'])
def index():
    channels = Channel.query.all()
    return render_template('index.html', channels=channels)

# LOGIN ROUTES

@app.route('/login', methods=["POST","GET"])
def login():
    return render_template('login.html')  

@app.route('/admin_login', methods=["POST","GET"])
def admin_login():
    form = CreateAdminForm()

    if form.validate_on_submit():
        print(form.name.data)
        print(form.username.data)
        print(form.password.data)


    return render_template('admin_login.html',form=form)    


# CHANNEL ROUTES

@app.route('/channel/<int:id>')
def channel(id):
    channel = Channel.query.filter_by(id=id).first()

    if channel is not None:
        return render_template('channel.html', channel=channel)
    else:
        print('Channel Not Found')
        return redirect('/')

@app.route('/create_channel', methods=['POST'])
def create_channel():
    
    channel_name = request.form['c_name']
    new_channel = Channel(name=channel_name)

    try:
        db.session.add(new_channel)
        db.session.commit()
        print('Channel Added')
        flash("Channel Created","success")
        return redirect(url_for('index'))

    except:
        return "There was an issue adding your task "

@app.route('/delete_channel/<int:id>')
def delete_channel(id):
    channel = Channel.query.filter_by(id=id).first()

    if channel is not None :
        db.session.delete(channel)
        db.session.commit()
        flash('Channel Deleted',"danger")
        return redirect('/')
    else:
        print('Channel Not Found')
        return redirect('/')

    new_channel = Channel(name=channel_name)

if __name__ == "__main__":
    app.run(debug=True)
