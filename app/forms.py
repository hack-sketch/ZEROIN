from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DateField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError , NumberRange
from app.models import User, Campaign, AdRequest,Sponsor, Influencer

class SponsorRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    company_name = StringField("Company Name", validators=[DataRequired()])
    industry = StringField("Industry", validators=[DataRequired()])
    budget = IntegerField("Budget", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

class InfluencerRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=[DataRequired()])
    niche = StringField("Platform", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    reach = IntegerField("Reach", validators=[DataRequired(), NumberRange(min=1)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class CampaignForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    start_date = DateField("Start Date", format="%Y-%m-%d", validators=[DataRequired()])
    end_date = DateField("End Date", format="%Y-%m-%d", validators=[DataRequired()])
    budget = IntegerField("Budget", validators=[DataRequired(), NumberRange(min=1)])
    visibility = SelectField("Visibility", choices=[("public", "Public"), ("private", "Private")], validators=[DataRequired()])
    goals = TextAreaField("Goals", validators=[DataRequired()])
    submit = SubmitField("Create Campaign")
    update = SubmitField("Update Campaign")

class AdRequestForm(FlaskForm):
    campaign_id = IntegerField("Campaign ID", validators=[DataRequired(), NumberRange(min=1)])
    influencer_id = IntegerField("Influencer ID", validators=[DataRequired(), NumberRange(min=1)])
    messages = TextAreaField("Messages")
    requirements = TextAreaField("Requirements", validators=[DataRequired()])
    payment_amount = IntegerField("Payment Amount", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Create Ad Request")
    update = SubmitField("Update Ad Request")

class AdminProfile(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)], default='')
    email = StringField('Email', validators=[DataRequired(), Email()], default='')
    submit = SubmitField('Update Profile')
    
class SponsorProfile(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)], default='')
    email = StringField('Email', validators=[DataRequired(), Email()], default='')
    company_name = StringField('Company Name', validators=[DataRequired()], default='')  
    submit = SubmitField('Update Profile')
    
class InfluencerProfile(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], default='')
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)], default='')
    email = StringField('Email', validators=[DataRequired(), Email()], default='')
    category = StringField('Category', validators=[DataRequired()], default='')
    social_media = StringField('Platform Link', validators=[DataRequired()], default='')
    submit = SubmitField('Update Profile')        
