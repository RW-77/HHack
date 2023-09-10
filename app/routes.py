from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import Schedule
from . import db
from utils.scrape_utils import extractor
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        print(len(request.files))
        pdf = request.files['pdf'] # flask request
        now = datetime.now()

        pdf_json = extractor(pdf); # list of dictionaries
        schedule = Schedule(date_generated=now, data=pdf_json)
        db.session.add(schedule)
        db.session.commit()

    return render_template("home.html", user=current_user)