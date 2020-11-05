from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms import LoginForm, RegistrationForm, CreateChannelForm, CreateSlotForm

login_manager = LoginManager()

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db,render_as_batch=True)

login_manager.init_app(app)
login_manager.login_view = "login"


# DATABASES
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
    bookings = db.relationship('Booking', backref='slot', lazy='dynamic')

    def __init__(self,start_time,end_time,channel_id):
        self.start_time = start_time
        self.end_time = end_time
        self.channel_id = channel_id
    
    def __repr__(self):
        return f"{self.start_time}hrs - {self.end_time}hrs"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    username = db.Column(db.String(64),unique=True)
    hashed_pass =db.Column(db.String(128))
    type = db.Column(db.Integer())
    bookings = db.relationship('Booking', backref='user',lazy='dynamic')
    last_logged_in = db.Column(db.DateTime)
    last_logged_out = db.Column(db.DateTime)


    def __init__(self,name,username,password,type):
        self.name = name
        self.username = username
        self.hashed_pass = generate_password_hash(password)
        self.type = type
    
    def check_password(self,password):
        return check_password_hash(self.hashed_pass,password)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer,db.ForeignKey('channel.id'))
    slot_id = db.Column(db.Integer,db.ForeignKey('slot.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    date = db.Column(db.Date)

    def __init__(self, channel_id, slot_id, user_id, date):
        self.channel_id = channel_id
        self.slot_id = slot_id
        self.user_id = user_id
        self.date = date
    
    def __repr__(self):
        return f"Booking ID: {self.id} Channel ID: {self.channel_id} Slot ID: {self.slot_id} User ID: {self.user_id} Date: {self.date}"


@app.route('/', methods=['POST','GET'])
def index():
    create_channel_form = CreateChannelForm()
    channels = Channel.query.all()
    return render_template('index.html', channels=channels, create_channel_form=create_channel_form)

# USER ROUTES

@app.route('/users')
def users():

    users = User.query.all()

    return render_template('users.html',users = users)

@app.route('/users/delete/<int:id>')
def delete_user(id):

    if current_user.type == 0 :

        user = User.query.get(id)

        if user is not None:
            db.session.delete(user)
            db.session.commit()
            flash("Account has been deleted","success")
            return redirect(url_for('users'))

    flash('Deleting user accounts is restricted to User Adminstrators',"danger")
    return redirect('index')



@app.route('/login', methods=["POST","GET"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()

        if user.check_password(form.password.data) and user is not None :
            login_user(user)
            # Set last logged in date and time
            user.last_logged_in = datetime.now()
            db.session.commit()

            flash("Logged In Successfully","success")

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('index')

            return redirect(next)
        else:
            flash("Unable to login",'danger')
            return redirect(url_for('login'))

    return render_template('login.html',form=form)  

@app.route('/register', methods=["POST","GET"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            name = form.name.data,
            username = form.username.data,
            password = form.password.data,
            type = form.type.data)
        db.session.add(user)
        db.session.commit()
        flash("Account has been created","success")
        return redirect(url_for('index'))   

    return render_template('register.html',form=form)

@app.route('/logout')
@login_required
def logout():
    user = User.query.filter_by(id = current_user.id).first()
    user.last_logged_out = datetime.now()
    db.session.commit()

    logout_user()

    flash('You have been logged out','info')
    return redirect(url_for('index'))



# SLOT ROUTES

@app.route('/slot/update',methods=['POST']) 
def slot_update():

    slot_id = request.form['slot_id']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    slot = Slot.query.filter_by(id=slot_id).first()

    if slot is not None :
        slot.start_time = start_time
        slot.end_time = end_time
        db.session.commit()
        flash('Slot Updated',"success")
        return redirect(url_for("channel",id=slot.channel_id))
    else:
        print('Slot Not Found')
        return redirect('/')

@app.route('/slot/delete/<int:id>',methods=['POST'])
def slot_delete(id):

    slot = Slot.query.filter_by(id=id).first()

    if slot is not None :
        channel = slot.channel_id
        db.session.delete(slot)
        db.session.commit()
        flash('Slot Deleted',"danger")
        return (url_for('channel',id=channel))
    else:
        flash('Error Deleting Slot',"danger")
        return redirect(url_for('index'))


# BOOKING ROUTES

@app.route('/book',methods=['POST'])
@login_required
def book():

    user_id = request.form['user_id']
    channel_id = request.form['channel_id']
    slot_id = request.form['slot_id']
    date = datetime.strptime(request.form['date'], "%Y-%m-%d")

    booking = Booking(user_id = user_id, channel_id = channel_id, slot_id = slot_id, date = date)
    db.session.add(booking)
    db.session.commit()

    flash("Booking has been created","success")
    return redirect(url_for('channel',id=channel_id))   

@app.route('/bookings')
@login_required
def bookings():

    user_id = current_user.id

    all_bookings = Booking.query.filter_by(user_id=user_id).all()

    return render_template('bookings.html', all_bookings=all_bookings)

@app.route('/bookings/delete/<int:id>')
@login_required
def delete_booking(id):

    user_id = current_user.id
    booking = Booking.query.filter_by(id=id).first()

    print(booking.user_id)


    if booking is not None and booking.user_id == user_id:
        db.session.delete(booking)
        db.session.commit()
        flash('Booking Has Been Deleted', "danger")
        return redirect(url_for('bookings'))






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
