from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+gaerdbms://root@/test?host=/cloudsql/clever-aleph-277201:us-central1:test"
# "mysql+mysqldb://root@/test?unix_socket=/cloudsql/<projectid>:<instancename>"



#### GOOOGLE SQL CODE ######
# # Google Cloud SQL (change this accordingly) 
# PASSWORD ="pass"
# PUBLIC_IP_ADDRESS ="34.70.107.99"
# DBNAME ="testdb"
# PROJECT_ID ="clever-aleph-277201"
# INSTANCE_NAME ="test"
  
# # configuration 
# app.config["SECRET_KEY"] = "yoursecretkey"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

# db = SQLAlchemy(app)

# # User ORM for SQLAlchemy 
# class Users(db.Model): 
#     id = db.Column(db.Integer, primary_key = True, nullable = False) 
#     name = db.Column(db.String(50), nullable = False) 
#     email = db.Column(db.String(50), nullable = False, unique = True) 
  
# @app.route('/add', methods =['POST']) 
# def add(): 
#     # geting name and email 
#     name = request.form.get('name') 
#     email = request.form.get('email') 
  
#     # checking if user already exists 
#     user = Users.query.filter_by(email = email).first() 
  
#     if not user: 
#         try: 
#             # creating Users object 
#             user = Users( 
#                 name = name, 
#                 email = email 
#             ) 
#             # adding the fields to users table 
#             db.session.add(user) 
#             db.session.commit() 
#             # response 
#             responseObject = { 
#                 'status' : 'success', 
#                 'message': 'Sucessfully registered.'
#             } 
  
#             return make_response(responseObject, 200) 
#         except: 
#             responseObject = { 
#                 'status' : 'fail', 
#                 'message': 'Some error occured !!'
#             } 
  
#             return make_response(responseObject, 400) 
          
#     else: 
#         # if user already exists then send status as fail 
#         responseObject = { 
#             'status' : 'fail', 
#             'message': 'User already exists !!'
#         } 
  
#         return make_response(responseObject, 403) 
  
# @app.route('/view') 
# def view(): 
#     # fetches all the users 
#     users = Users.query.all() 
#     # response list consisting user details 
#     response = list() 
  
#     for user in users: 
#         response.append({ 
#             "name" : user.name, 
#             "email": user.email 
#         }) 
  
#     return make_response({ 
#         'status' : 'success', 
#         'message': response 
#     }, 200) 
  
  
# if __name__ == "__main__": 
#     # serving the app directly 
#     app.run(debug=True) 

class Channel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<Task %r>'% self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == "POST":
        channel_name = request.form['c_name']
        new_channel = Channel(name=channel_name)

        try:
            db.session.add(new_channel)
            db.session.commit()
            print('Item Added')
            return redirect('/')

        except:
            return "There was an issue adding your task "
    else:
        channels = Channel.query.all()
        return render_template('index.html', channels=channels)

@app.route('/login')
def login():
    return render_template('login.html')    


if __name__ == "__main__":
    app.run(debug=True)