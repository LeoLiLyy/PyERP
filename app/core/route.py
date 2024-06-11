from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from flask_login import login_user, logout_user, login_required, current_user
from app.translations import load_translations  # Correct import
from markupsafe import escape
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


@login_required
@core_bp.route("/admin")
def admin_panel():
    from app.auth.route import f_email, users_online
    global is_admin, user
    is_admin = False
    # admin check
    if f_email == 'admin@example.com':
        is_admin = True
        return render_template("./html/core/admin/admin_dashboard.html", user_list=escape(users_online))
    else:
        # requests.post("http://localhost:80/erp_admin_ntfy",
        #               data="Illegal login attempt to admin panel detected".encode(encoding='utf-8'))
        logout_user()
        return redirect("/", 403)


@core_bp.route('/user_manager', methods=['GET', 'POST'])
def user_manager():
    from app.models import Employee
    from app.auth.route import f_email, users_online
    if is_admin:
        # button detection
        user_id = request.form.get('user_id')
        action = request.form.get('action')
        submit = request.form.get('submit')

        all_users = Employee.query.all()
        for l_users in all_users:
            l_users.is_online = l_users.Email in users_online
        if user_id:
            if action == 'kick':
                return kick_user(user_id)
            elif action == 'edit':
                return redirect('/edit_user/' + user_id)
            elif action == 'delete':
                return delete_user(user_id)
            else:
                return redirect("/user_manager")
        return render_template('./html/core/admin/user_manager.html', users=all_users)
    else:
        # requests.post("http://localhost:80/erp_admin_ntfy",
        #               data="Illegal login attempt to admin panel detected".encode(encoding='utf-8'))
        logout_user()
        return redirect("/")


def kick_user(user_id):
    from app.models import Employee
    user_k = Employee.query.get(user_id)
    if user_k:
        user_k.session_token = None
        db.session.commit()
        logger.info("[*] Kicked user with ID: " + str(user_id))
    return redirect("/core/user_manager")


@core_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    from app.models import Employee
    e_user = Employee.query.get(user_id)
    if request.method == 'POST':
        db.session.add(e_user)
        e_user.Name = request.form.get('name')
        e_user.Dept = request.form.get('dept')
        e_user.Email = request.form.get('email')
        e_user.Password = hashlib.sha256(request.form.get('password').encode('utf-8')).hexdigest()
        e_user.session_token = None
        db.session.commit()
        return redirect('/core/user_manager')
    return render_template('./html/core/admin/edit_user.html', user=e_user)


def delete_user(user_id):
    from app.models import Employee
    d_user = Employee.query.get(user_id)
    d_user.Password = 'invalid'
    d_user.session_token = None
    db.session.commit()
    logger.info("[*] Deleted user with ID: " + str(user_id))
    return redirect("/core/user_manager")


@core_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
# creating new users
def create_user():
    from app.models import Employee
    if request.method == 'POST':
        id = request.form.get('employeeId')
        name = request.form.get('name')
        dept = request.form.get('dept')
        email = request.form.get('email')
        # hashing the users password before it enters the database
        password = hashlib.sha256(str(request.form.get('password')).encode('utf-8')).hexdigest()
        new_user = Employee(EmployeeID=id, Name=name, Dept=dept, Email=email, Password=password, session_token=None)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/core/user_management')  # Redirect to a user management page
    return render_template('./html/core/admin/create_user.html')
