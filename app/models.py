from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user') # "admin", "sponsor", "influencer"
    sponsors = db.relationship('Sponsor', backref='user', lazy=True)
    influencers = db.relationship('Influencer', backref='user', lazy=True)  
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)

    def __repr__(self):
        return f"Sponsor('{self.company_name}', '{self.industry}', '{self.budget}')"

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    niche = db.Column(db.String(100), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)
    
    def __repr__(self):
        return f"Influencer('{self.name}', '{self.category}', '{self.niche}', '{self.reach}')"

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.String(10), nullable=False, default='public')
    goals = db.Column(db.String(500), nullable=True)
    flagged = db.Column(db.Boolean, default=False)
    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)

    def __repr__(self):
        return f"Campaign('{self.name}', '{self.start_date}', '{self.end_date}')"

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    messages = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.String(500), nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')   # "Pending", "Accepted", "Rejected"

    def __repr__(self):
        return f"AdRequest('{self.campaign_id}', '{self.influencer_id}', '{self.status}')"

