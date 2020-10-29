from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField
from wtforms.validators import Required
from wtforms.fields.html5 import DateField



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

class CreateChannelForm(FlaskForm):
    name = StringField('Desired Channel Name')
    date = DateField('Channel Start Date', format='%Y-%m-%d')
    submit = SubmitField('Submit')

class CreateSlotForm(FlaskForm):
    channel_id = HiddenField()
    start_time = StringField("Start Time")
    end_time = StringField('End Time')
    submit = SubmitField('Submit')


class Channel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    slots = db.relationship('Slot', backref='channel',lazy='dynamic')

    def __init__(self, name, start_date):
        self.name = name
        self.start_date = start_date

    def __repr__(self):
        return '<Task %r>'% self.id

class Slot(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    start_time = db.Column(db.String(4))
    end_time = db.Column(db.String(4))
    channel_id = db.Column(db.Integer,db.ForeignKey('channel.id'))

    def __init__(self,start_time,end_time,channel_id):
        self.start_time = start_time
        self.end_time = end_time
        self.channel_id = channel_id
    
    def __repr__(self):
        return f"{self.start_time}hrs - {self.end_time}hrs"


class Admin(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50))


@app.route('/', methods=['POST','GET'])
def index():
    create_channel_form = CreateChannelForm()

    channels = Channel.query.all()
    return render_template('index.html', channels=channels, create_channel_form=create_channel_form)

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

@app.route('/channel/<int:id>', methods=["POST","GET"])
def channel(id):
    channel = Channel.query.filter_by(id=id).first()
    form = CreateSlotForm()

    if channel is not None:
        if form.validate_on_submit():
            channel_id = form.channel_id.data
            start_time = form.start_time.data
            end_time = form.end_time.data

            new_slot = Slot(start_time=start_time,end_time=end_time, channel_id=channel_id)
            try:
                db.session.add(new_slot)
                db.session.commit()
                print('Slot Added')
                flash("Slot Created","success")
                return redirect(url_for('channel',id=channel_id))

            except:
                return "There was an issue adding your task "


        return render_template('channel.html', channel=channel, form=form)
    else:
        print('Channel Not Found')
        return redirect('/')

@app.route('/create_channel', methods=['POST'])
def create_channel(): 

    form = CreateChannelForm()

    if form.validate_on_submit():
        channel_name = form.name.data
        start_date = form.date.data
        new_channel = Channel(name=channel_name, start_date=start_date)

        try:
            db.session.add(new_channel)
            db.session.commit()
            print('Channel Added')
            flash("Channel Created","success")
            return redirect(url_for('index'))

        except:
            return "There was an issue adding your task "
    else:
        flash("Failed to create channel","danger")
        return redirect(url_for('index'))

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
