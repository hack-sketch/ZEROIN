from flask import render_template, url_for, flash, redirect, request, Flask
from app import app, db, bcrypt
from app.forms import LoginForm, SponsorRegistrationForm, InfluencerRegistrationForm, CampaignForm, AdRequestForm, AdminProfile, SponsorProfile, InfluencerProfile
from app.models import User, Sponsor, Influencer, Campaign, AdRequest
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from collections import defaultdict
from sqlalchemy import func

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")
    
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register/sponsor", methods=["GET", "POST"])
def register_sponsor():
    form = SponsorRegistrationForm()
    user1 = User.query.filter(User.username==form.username.data).first()
    user2 = User.query.filter(User.email==form.email.data).first()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role="sponsor", created_at=datetime.now())
        db.session.add(user)
        db.session.commit()
        sponsor = Sponsor(user_id=user.id, company_name=form.company_name.data, industry=form.industry.data, budget=form.budget.data)
        db.session.add(sponsor)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("login"))
    elif (user1): 
        return render_template("register_sponsor.html", form=form , error="That username is taken. Please choose a different one.")
    elif (user2): 
        return render_template("register_sponsor.html", form=form , error="That email is taken. Please choose a different one.")
    return render_template("register_sponsor.html", form=form)

@app.route("/register/influencer", methods=["GET", "POST"])
def register_influencer():
    form = InfluencerRegistrationForm()
    user1 = User.query.filter(User.username==form.username.data).first()
    user2 = User.query.filter(User.email==form.email.data).first()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role="influencer", created_at=datetime.now())
        db.session.add(user)
        db.session.commit()
        influencer = Influencer(user_id=user.id, name=form.name.data,niche=form.niche.data ,category=form.category.data, reach=form.reach.data)
        db.session.add(influencer)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("login"))
    elif (user1): 
        return render_template("register_influencer.html", form=form , error="That username is taken. Please choose a different one.")
    elif (user2): 
        return render_template("register_influencer.html", form=form , error="That email is taken. Please choose a different one.")
    return render_template("register_influencer.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if current_user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            elif current_user.role == "sponsor":
                return redirect(url_for("sponsor_dashboard"))
            elif current_user.role == "influencer":
                return redirect(url_for("influencer_dashboard"))   
            return redirect(next_page) if next_page else redirect(url_for("home"))
            
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
            return render_template("login.html", form=form, title="Login" , error="Login Unsuccessful. Please check email and password!!")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'sponsor':
        return redirect(url_for('sponsor_dashboard'))
    elif current_user.role == 'influencer':
        return redirect(url_for('influencer_dashboard'))
    else:
        return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.id)
    if user.role == 'admin':
        form = AdminProfile()
    elif user.role == 'sponsor':
        form = SponsorProfile()
    elif user.role == 'influencer':
        form = InfluencerProfile()
                            
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        
        if user.role == 'sponsor':
            sponsor=Sponsor.query.filter(Sponsor.user_id==user.id).first()
            sponsor.company_name = form.company_name.data
        elif user.role == 'influencer': 
            influencer=Influencer.query.filter(Influencer.user_id==user.id).first()
            influencer.niche = form.social_media.data
            influencer.name = form.name.data
            influencer.category = form.category.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return render_template('profile.html', form=form , user=user, msg="Your Profile has been updated.") 
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        
        if user.role == 'sponsor':
            sponsor=Sponsor.query.filter(Sponsor.user_id==user.id).first()
            form.company_name.data = sponsor.company_name
        elif user.role == 'influencer': 
            influencer=Influencer.query.filter(Influencer.user_id==user.id).first()
            form.social_media.data =  influencer.niche
            form.name.data = influencer.name   
            form.category.data = influencer.category
    return render_template('profile.html', form=form, user=user)

@app.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return redirect(url_for("home"))
    campaigns = Campaign.query.all()
    return render_template("admin_dashboard.html", campaigns=campaigns) 
    
@app.route("/admin/info")
@login_required
def admin_dashboard_info():
    if current_user.role != "admin":
        return redirect(url_for("home"))

    active_sponsors = Sponsor.query.count()
    active_influencers = Influencer.query.count()
    active_admins = User.query.filter_by(role="admin").count()

    public_campaigns = Campaign.query.filter_by(visibility="public").count()
    private_campaigns = Campaign.query.filter_by(visibility="private").count()
    total_campaigns = Campaign.query.count()

    pending_requests = AdRequest.query.filter_by(status="Pending").count()
    accepted_requests = AdRequest.query.filter_by(status="Accepted").count()
    rejected_requests = AdRequest.query.filter_by(status="Rejected").count()

    flagged_sponsors = Sponsor.query.filter_by(flagged=True).count()
    flagged_influencers = Influencer.query.filter_by(flagged=True).count()
    flagged_campaigns = Campaign.query.filter_by(flagged=True).count()

    return render_template(
        "admin_dashboard_info.html",
        active_sponsors=active_sponsors,
        active_influencers=active_influencers,
        active_admins=active_admins,
        public_campaigns=public_campaigns,
        private_campaigns=private_campaigns,
        total_campaigns=total_campaigns,
        pending_requests=pending_requests,
        accepted_requests=accepted_requests,
        rejected_requests=rejected_requests,
        flagged_sponsors=flagged_sponsors,
        flagged_influencers=flagged_influencers,
        flagged_campaigns=flagged_campaigns
    )    
    
@app.route('/admin/chart')
@login_required
def chart():
    sponsor_registrations = db.session.query(
        func.date(User.created_at), func.count(User.id)
    ).join(Sponsor).group_by(func.date(User.created_at)).all()

    influencer_registrations = db.session.query(
        func.date(User.created_at), func.count(User.id)
    ).join(Influencer).group_by(func.date(User.created_at)).all()

    # Dictionary me dalna hai
    registration_data = defaultdict(lambda: {'sponsors': 0, 'influencers': 0})

    for date, count in sponsor_registrations:
        registration_data[date]['sponsors'] = count

    for date, count in influencer_registrations:
        registration_data[date]['influencers'] = count

    labels = []
    sponsor_counts = []
    influencer_counts = []

    for date in sorted(registration_data.keys()):
        if isinstance(date, str):
            labels.append(date)
        else:
            labels.append(date.strftime("%Y-%m-%d"))
            
        sponsor_counts.append(registration_data[date]['sponsors'])
        influencer_counts.append(registration_data[date]['influencers'])

    return render_template('chart.html', labels=labels, sponsor_counts=sponsor_counts, influencer_counts=influencer_counts)  
    
@app.route('/admin/search', methods=['GET'])
@login_required
def admin_search():
    filter_type = request.args.get('filter', 'influencer')
    search_query = request.args.get('search', '')

    results = []
    if filter_type == 'influencer':
        results = Influencer.query.filter(Influencer.name.like(f'%{search_query}%')).all() if search_query else Influencer.query.all()
    elif filter_type == 'sponsor':
        results = Sponsor.query.filter(Sponsor.company_name.like(f'%{search_query}%')).all() if search_query else Sponsor.query.all()
    elif filter_type == 'campaign':
        results = Campaign.query.filter(Campaign.name.like(f'%{search_query}%')).all() if search_query else Campaign.query.all()

    return render_template('admin_search.html', results=results, filter=filter_type)

@app.route('/flag_entry/<int:entry_id>', methods=['POST'])
@login_required
def flag_entry(entry_id):
    filter_type = request.args.get('filter', 'influencer')

    if filter_type == 'influencer':
        entry = Influencer.query.get_or_404(entry_id)
    elif filter_type == 'sponsor':
        entry = Sponsor.query.get_or_404(entry_id)
    elif filter_type == 'campaign':
        entry = Campaign.query.get_or_404(entry_id)
    
    entry.flagged = True
    db.session.commit()
    
    return redirect(url_for('admin_search', filter=filter_type))

@app.route('/flagged_users', methods=['GET'])
@login_required
def flagged_users():
    flagged_influencers = Influencer.query.filter_by(flagged=True).all()
    flagged_sponsors = Sponsor.query.filter_by(flagged=True).all()
    flagged_campaigns = Campaign.query.filter_by(flagged=True).all()

    flagged_entries = []
    for influencer in flagged_influencers:
        flagged_entries.append((influencer, 'influencer'))
    for sponsor in flagged_sponsors:
        flagged_entries.append((sponsor, 'sponsor'))
    for campaign in flagged_campaigns:
        flagged_entries.append((campaign, 'campaign'))

    return render_template('flagged_users.html', flagged_entries=flagged_entries)

@app.route('/remove_flag/<int:entry_id>/<string:filter>', methods=['GET'])
@login_required
def remove_flag(entry_id, filter):
    if filter == 'influencer':
        entry = Influencer.query.get_or_404(entry_id)
    elif filter == 'sponsor':
        entry = Sponsor.query.get_or_404(entry_id)
    elif filter == 'campaign':
        entry = Campaign.query.get_or_404(entry_id)
    
    entry.flagged = False
    db.session.commit()
    flash('Flag has been removed.', 'success')
    return redirect(url_for('flagged_users'))
   
    
@app.route("/sponsor")
@login_required
def sponsor_dashboard():
    if current_user.role != "sponsor":
        return redirect(url_for("home"))
    return render_template("sponsor_dashboard.html", title="Sponsor Dashboard")

@app.route("/sponsor/campaign/new", methods=['GET', 'POST'])
def new_campaign_sponsor():
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            visibility=form.visibility.data,
            goals=form.goals.data,
            sponsor_id=current_user.id
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign has been created!', 'success')
        return redirect(url_for('manage_campaign_sponsor'))
    return render_template('create_campaign.html', form=form, endpoint=f'/sponsor/campaign/new')

@app.route("/sponsor/campaign/manage", methods=['GET', 'POST'])
def manage_campaign_sponsor():
    campaigns = Campaign.query.filter(Campaign.sponsor_id==current_user.id).all()
    return render_template("sponsor_campaigns.html", campaigns=campaigns)

@app.route("/sponsor/campaign/<int:campaign_id>/update", methods=['GET', 'POST'])
def update_campaign_sponsor(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = CampaignForm()
    if form.validate_on_submit():
        campaign.name = form.name.data
        campaign.description = form.description.data
        campaign.start_date = form.start_date.data
        campaign.end_date = form.end_date.data
        campaign.budget = form.budget.data
        campaign.visibility = form.visibility.data
        campaign.goals = form.goals.data
        db.session.commit()
        flash('Campaign has been updated!', 'success')
        return redirect(url_for('manage_campaign_sponsor'))
    elif request.method == 'GET':
        form.name.data = campaign.name
        form.description.data = campaign.description
        form.start_date.data = campaign.start_date
        form.end_date.data = campaign.end_date
        form.budget.data = campaign.budget
        form.visibility.data = campaign.visibility
        form.goals.data = campaign.goals
    return render_template('create_campaign.html', form=form)

@app.route("/sponsor/campaign/<int:campaign_id>/delete", methods=['POST'])
def delete_campaign_sponsor(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    ad_requests=AdRequest.query.filter(AdRequest.campaign_id==campaign.id).all()
    for ad in ad_requests:
        db.session.delete(ad)
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign has been deleted!', 'success')
    return redirect(url_for('manage_campaign_sponsor'))

@app.route("/sponsor/ad_request/new", methods=['GET', 'POST'])
def new_ad_request():
    form = AdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in Campaign.query.filter_by(sponsor_id=current_user.id).all()]
    form.influencer_id.choices = [(influencer.id, influencer.name) for influencer in Influencer.query.all()]
    
    if form.validate_on_submit():
        ad_request = AdRequest(
            sponsor_id = current_user.id,
            campaign_id=form.campaign_id.data,
            influencer_id=form.influencer_id.data,
            messages=form.messages.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data
        )
        db.session.add(ad_request)
        db.session.commit()
        flash('Ad Request has been created!', 'success')
        return redirect(url_for('edit_ad_requests'))
    return render_template('create_ad_request.html', form=form, endpoint=f'/sponsor/ad_request/new')

@app.route("/sponsor/ad_requests")
def edit_ad_requests():
    ad_requests = AdRequest.query.filter(AdRequest.sponsor_id==current_user.id).all()
    return render_template('sponsor_ad_requests.html', ad_requests=ad_requests)

@app.route("/sponsor/ad_request/<int:ad_request_id>/update", methods=['GET', 'POST'])
def update_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    form = AdRequestForm()

    if form.validate_on_submit():
        ad_request.campaign_id = form.campaign_id.data
        ad_request.influencer_id = form.influencer_id.data
        ad_request.messages = form.messages.data
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        db.session.commit()
        flash('Ad Request has been updated!', 'success')
        return redirect(url_for('edit_ad_requests'))
    elif request.method == 'GET':
        form.campaign_id.data = ad_request.campaign_id
        form.influencer_id.data = ad_request.influencer_id
        form.messages.data = ad_request.messages
        form.requirements.data = ad_request.requirements
        form.payment_amount.data = ad_request.payment_amount
    return render_template('create_ad_request.html', form=form)

@app.route("/sponsor/ad_request/<int:ad_request_id>/delete", methods=['POST'])
def delete_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request:
        db.session.delete(ad_request)
        db.session.commit()
        flash('Ad request has been deleted successfully!', 'success')
    else:
        flash('Ad request not found.', 'danger')
    return redirect(url_for('edit_ad_requests'))

@app.route("/sponsor/ad_request/<int:ad_request_id>/negotiate", methods=['GET', 'POST'])
def negotiate_sponsor(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if request.method == 'POST':
        new_payment_amount = request.form.get('payment_amount')
        ad_request.payment_amount = new_payment_amount
        db.session.commit()
        flash('Payment amount has been negotiated!', 'success')
        return redirect(url_for('edit_ad_requests'))
    return render_template('negotiate_amount.html', ad_request=ad_request)

@app.route("/sponsor/search_influencers", methods=['GET', 'POST'])
def search_influencers():
    query = request.args.get('query')
    if query:
        influencers = Influencer.query.filter((Influencer.niche.ilike(f"%{query}%")) | (Influencer.id.ilike(f"%{query}%"))| (Influencer.category.ilike(f"%{query}%")) | (Influencer.name.ilike(f"%{query}%")), Influencer.flagged==False).all()
    else:
        influencers = Influencer.query.filter(Influencer.flagged==False).all()
    return render_template('search_influencers.html', influencers=influencers)

@app.route("/influencer")
@login_required
def influencer_dashboard():
    if current_user.role != "influencer":
        return redirect(url_for("home"))
    return render_template("influencer_dashboard.html", title="Influencer Dashboard")

@app.route("/influencer/search_campaigns", methods=['GET', 'POST'])
def search_campaigns():
    query=request.args.get('query')
    if query:
        campaigns = Campaign.query.filter((Campaign.name.ilike(f"%{query}%")) | (Campaign.goals.ilike(f"%{query}%")),Campaign.visibility=='public', Campaign.flagged==False).all()
    else:
        campaigns = Campaign.query.filter(Campaign.visibility=='public', Campaign.flagged==False).all()
    return render_template('search_campaigns.html', campaigns=campaigns)


@app.route("/influencer/ad_requests")
def view_ad_requests():
    influencer = Influencer.query.filter(Influencer.user_id == current_user.id).first()
    ad_requests = AdRequest.query.filter_by(status='Pending',influencer_id=influencer.id).all()
    return render_template('influencer_ad_requests.html', ad_requests=ad_requests, status='Pending')

@app.route("/influencer/ad_request/<int:ad_request_id>/accept")
def accept_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    ad_request.status = 'Accepted'
    db.session.commit()
    flash('You have accepted the ad request.', 'success')
    return redirect(url_for('view_ad_requests'))

@app.route("/influencer/ad_request/<int:ad_request_id>/reject")
def reject_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    ad_request.status = 'Rejected'
    db.session.commit()
    flash('You have rejected the ad request.', 'success')
    return redirect(url_for('view_ad_requests'))

@app.route("/influencer/ad_request/<int:ad_request_id>/negotiate", methods=['GET', 'POST'])
def negotiate_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if request.method == 'POST':
        new_payment_amount = request.form.get('payment_amount')
        ad_request.payment_amount = new_payment_amount
        db.session.commit()
        flash('Payment amount has been negotiated!', 'success')
        return redirect(url_for('view_ad_requests'))
    return render_template('negotiate_amount.html', ad_request=ad_request)

@app.route("/influencer/accepted_ad_requests")
def accepted_ad_requests():
    influencer = Influencer.query.filter(Influencer.user_id == current_user.id).first()
    ad_requests = AdRequest.query.filter_by(status='Accepted',influencer_id=influencer.id).all()
    return render_template('influencer_ad_requests.html', ad_requests=ad_requests, status='Accepted')

@app.route("/influencer/rejected_ad_requests")
def rejected_ad_requests():
    influencer = Influencer.query.filter(Influencer.user_id == current_user.id).first()
    ad_requests = AdRequest.query.filter_by(status='Rejected',influencer_id=influencer.id).all()
    return render_template('influencer_ad_requests.html', ad_requests=ad_requests, status='Rejected')
