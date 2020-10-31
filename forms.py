from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
# FORMS 

class RegistrationForm(FlaskForm):
    name = StringField("Whats your preferred name", validators=[DataRequired()])
    username = StringField("Desired Username?",validators=[DataRequired()])
    password = PasswordField('Desired Password?',validators=[DataRequired()])
    type = RadioField('User Type', choices=[(0,"User Administrator"),(1,"Staff User"),(2,"Student User")])
    submit = SubmitField('Submit')

class CreateChannelForm(FlaskForm):
    name = StringField('Desired Channel Name',validators=[DataRequired()])
    date = DateField('Channel Start Date', format='%Y-%m-%d',validators=[DataRequired()])
    submit = SubmitField('Submit')

class CreateSlotForm(FlaskForm):
    channel_id = HiddenField()
    start_time = StringField("Start Time", validators=[DataRequired()])
    end_time = StringField('End Time', validators=[DataRequired()])
    submit = SubmitField('Submit')