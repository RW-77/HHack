from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Schedule
from operator import itemgetter
from . import db
from utils.scrape_utils import extractor, generate
from datetime import datetime, timedelta, date
import time

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    now = datetime.now()
    # now_weekday = date.today().weekday()
    now_weekday = 1
    slots = []
    schedule = Schedule.query.filter_by(user_id=current_user.id).one().data
    day_schedule = schedule[now_weekday]
    day_schedule.sort(key = itemgetter('Start'), reverse=False)
    print(day_schedule)
    for i in range(len(day_schedule)-1):
        print(day_schedule)
        last_class = datetime.strptime(day_schedule[i]["End"], "%H:%M")
        next_class = datetime.strptime(day_schedule[i+1]["Start"], "%H:%M")
        print(next_class-last_class >= timedelta(minutes=90))
        if(next_class-last_class >= timedelta(minutes=90)):
            slots.append({
                "start": day_schedule[i]["End"],
                "end": day_schedule[i+1]["Start"],
                "start_building": day_schedule[i]["Building"],
                "end_building": day_schedule[i+1]["Building"],
                "start_name": day_schedule[i]["Class"],
                "end_name": day_schedule[i+1]["Class"]
            })
    images = generate(day_schedule)
    return render_template("home.html", user=current_user, slots=slots, images=images)


@routes.route('/upload', methods=['GET', 'POST']) # upload page
@login_required
def upload():
    if request.method == 'POST':
        pdf = request.files['pdf'] # flask request
        now = datetime.now()

        pdf_json = extractor(pdf); # list of dictionaries
        print("hi again")
        schedule = Schedule(date_generated=now, data=pdf_json, user_id=current_user.id)
        db.session.add(schedule)
        db.session.commit()
        flash('Schedule uploaded successfully!', category='success')
        time.sleep(2) # so the user can see the success banner
        # should then take user to home page
        return redirect(url_for('routes.home')) # should always redir to home page after upload

    return render_template("upload.html", user=current_user)