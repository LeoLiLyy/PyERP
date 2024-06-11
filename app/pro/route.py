from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from flask_login import login_user, logout_user, login_required, current_user
from app.translations import load_translations
from app.models import Inventory, db, Project
import os
import requests
import logging
from pathlib import Path
from datetime import date

product_bp = Blueprint('product', __name__)

logger = logging.getLogger('product')


@product_bp.route("/design")
@login_required
def design():
    return render_template("html/design/design.html")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@product_bp.route("/new_design", methods=["GET", "POST"])
@login_required
def new_design():
    projects = Project.query.all()
    if request.method == "POST":
        p_name = request.form.get("productName")
        p_detail = request.form.get("designDetails")
        if 'fileUpload' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['fileUpload']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        file = request.files.get('fileUpload')
        if file:
            file_path = os.path.join('../uploads', file.filename)
            file.save(file_path)
        else:
            file_path = None
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template("html/design/new_design.html", projects=projects)
