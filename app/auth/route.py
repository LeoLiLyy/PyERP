from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from flask_login import login_user, logout_user, login_required, current_user
from app.translations import load_translations  # Correct import
import hashlib
import os
import requests
import logging

global f_email

auth_bp = Blueprint('auth', __name__)

logger = logging.getLogger('auth')

# Use the secret key from your Google reCAPTCHA registration
RECAPTCHA_SECRET_KEY = '6LfKCfUpAAAAAD8T-9thLK60OxvPTYdNCEuby0ql'

users_online = []


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    global user, f_email
    if request.method == 'POST':
        f_email = request.form['email']
        recaptcha_response = request.form['g-recaptcha-response']
        password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        from app.models import Employee, db
        user = Employee.query.filter_by(Email=f_email, Password=password).first()

        logger.debug("[!] List of users detected:" + str(user))

        # Validate reCAPTCHA response
        data = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        validation_response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        validation_result = validation_response.json()

        if validation_result['success']:
            if user:
                logger.info("[*] " + str(request.form["email"]) + " is now logged in!")
                login_user(user, remember=request.form.get('remember', 'false').lower() in ['true', '1', 't'])
                users_online.append(f_email)
                session_token = os.urandom(24).hex()
                user.session_token = session_token
                db.session.commit()
                session['user_token'] = session_token
                return redirect('/core/dashboard')
            else:
                logger.warning("Illegal login attempt (typo & wrong credentials) detected")
                flash(g.translations['Invalid username or password.'])
                return render_template('./html/auth/login.html')
        else:
            # Handle reCAPTCHA validation failure
            logger.warning("Illegal login attempt (bot) detected")
            flash(g.translations['reCAPTCHA validation failed.'])
            return render_template('./html/auth/login.html')
    return render_template('./html/auth/login.html')


@login_required
@auth_bp.route("/logout")
def logout():
    global f_email, db
    users_online.remove(f_email)
    from app.models import Employee, db
    user_fil = Employee.query.filter_by(EmployeeID=current_user.get_id()).first()
    if user_fil:
        user_fil.session_token = None
        db.session.commit()
    session.pop('user_token', None)
    logout_user()
    logger.info("[*] " + str(f_email) + " is now logged out")
    return redirect("/")
