from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Schedule
from . import db
from utils.scrape_utils import extractor
from datetime import datetime
import time

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    

    return render_template("home.html", user=current_user)


@routes.route('/upload', methods=['GET', 'POST']) # upload page
@login_required
def upload():
    if request.method == 'POST':
        print(len(request.files))
        pdf = request.files['pdf'] # flask request
        now = datetime.now()

        pdf_json = extractor(pdf); # list of dictionaries
        schedule = Schedule(date_generated=now, data=pdf_json)
        db.session.add(schedule)
        db.session.commit()
        flash('Schedule uploaded successfully!', category='success')
        time.sleep(2) # so the user can see the success banner
        # should then take user to home page
        return redirect(url_for('routes.home')) # should always redir to home page after upload

    return render_template("upload.html", user=current_user)