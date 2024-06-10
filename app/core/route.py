from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Employee, db  # Ensure you have a User model in your models.py
from app.translations import load_translations  # Correct import
import hashlib
import os
import requests
import logging

core_bp = Blueprint('core', __name__)

logger = logging.getLogger('core')

# Welcome page / Homepage
@core_bp.route("/welcome")
def welcome_page():
    return render_template('./html/core/welcome.html')


# Login Page

@login_required
@core_bp.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    # checking if the current user is authenticated and NOT give them access to the dashboard containing classified
    # datas
    if current_user.is_authenticated:
        return render_template("./html/core/dashboard.html")
    else:
        return redirect("/")