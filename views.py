from flask import render_template, request, redirect, url_for, flash
from app import app
from Tuning import generate_study_plan

@app.route('/personalized_study_plan', methods=['GET', 'POST'])
def personalized_study_plan():
    if request.method == 'POST':
        study_details = request.form['study_details']
        study_plan = generate_study_plan(study_details)
        return render_template('study_plan.html', study_plan=study_plan)
    return render_template('personalized_study_plan.html')
