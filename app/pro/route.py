from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.translations import load_translations
from app.models import Inventory, db, Project, Design
import os
import requests
import logging
from pathlib import Path
from datetime import date

product_bp = Blueprint('product', __name__)

logger = logging.getLogger('product')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


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
        if file and allowed_file(file.filename):
            filename = file.filename
            upload_folder = os.path.join(current_app.root_path, 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            # Save design details to the database
            new_design = Design(product_name=p_name, design_details=p_detail, project_id=request.form.get('projectId'), file_path=file_path)
            db.session.add(new_design)
            db.session.commit()
            flash('Design submitted successfully!', 'success')
            return redirect(url_for('product.design'))
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template("html/design/new_design.html", projects=projects)