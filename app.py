from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Channel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<Task %r>'% self.id

@app.route('/', methods=['POST','GET'])
def index():
    channels = Channel.query.all()
    return render_template('index.html', channels=channels)

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
        flash("Channel Created")
        return redirect(url_for('index'))

    except:
        return "There was an issue adding your task "

@app.route('/delete_channel/<int:id>')
def delete_channel(id):
    channel = Channel.query.filter_by(id=id).first()

    if channel is not None :
        db.session.delete(channel)
        db.session.commit()
        flash('Channel Deleted')
        return redirect('/')
    else:
        print('Channel Not Found')
        return redirect('/')



    new_channel = Channel(name=channel_name)



@app.route('/login')
def login():
    return render_template('login.html')    


if __name__ == "__main__":
    app.run(debug=True)