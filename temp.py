from solana.rpc.api import Client
from spl.token.client import Token
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from markupsafe import escape
from flask import redirect
from flask import session
from flask import request
from flask import render_template
from flask import Flask
from flask import blueprints
import flask
from werkzeug.utils import secure_filename
import logging
import colorlog
import json
from datetime import date
import time
import secrets
import requests
import hashlib
import matplotlib

matplotlib.use('Agg')
# Use the non-GUI backend to generate plots in order to fix the bug where system will crash when
# importing matplotlib
import matplotlib.pyplot as plt
import os
from ftplib import FTP
from pathlib import Path
from extensions.language_manager import LanguageManager, _


logger.info("[!] Server started or reloaded")


# requests.post("http://localhost:80/erp_admin_ntfy",
#               data="Server started or reloaded".encode(encoding='utf-8'))

# Welcome page / Homepage
@app.route("/")
def welcome_page():
    return render_template('html/welcome.html')


# Login Page

@login_required
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    # checking if the current user is authenticated and NOT give them access to the dashboard containing classified
    # datas
    if current_user.is_authenticated:
        return render_template("html/dashboard.html")
    else:
        return redirect("/")


@login_required
@app.route("/admin")
def admin_panel():
    global is_admin, user, email
    is_admin = False
    with open('datas/settings.json', 'r') as s_f:
        settings = json.loads(s_f.read())
        # admin check
        if user and settings["Admin"] == email:
            is_admin = True
            return render_template("html/admin_dashboard.html", user_list=users_online)
        else:
            # requests.post("http://localhost:80/erp_admin_ntfy",
            #               data="Illegal login attempt to admin panel detected".encode(encoding='utf-8'))
            logout_user()
            return redirect("/", 403)
        s_f.close()


@app.route('/user_manager', methods=['GET', 'POST'])
def user_manager():
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
        return render_template('html/user_manager.html', users=all_users)
    else:
        # requests.post("http://localhost:80/erp_admin_ntfy",
        #               data="Illegal login attempt to admin panel detected".encode(encoding='utf-8'))
        logout_user()
        return redirect("/")


def kick_user(user_id):
    user_k = Employee.query.get(user_id)
    if user_k:
        user_k.session_token = None
        db.session.commit()
        logger.info("[*] Kicked user with ID: " + str(user_id))
    return redirect("/user_manager")


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    e_user = Employee.query.get(user_id)
    if request.method == 'POST':
        db.session.add(e_user)
        e_user.Name = request.form.get('name')
        e_user.Dept = request.form.get('dept')
        e_user.Email = request.form.get('email')
        e_user.Password = hashlib.sha256(request.form.get('password').encode('utf-8')).hexdigest()
        e_user.session_token = None
        db.session.commit()
        return redirect('/user_manager')
    return render_template('html/edit_user.html', user=e_user)


def delete_user(user_id):
    d_user = Employee.query.get(user_id)
    d_user.Password = 'invalid'
    d_user.session_token = None
    db.session.commit()
    logger.info("[*] Deleted user with ID: " + str(user_id))
    return redirect("/user_manager")


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
# creating new users
def create_user():
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
        return redirect('/user_management')  # Redirect to a user management page
    return render_template('/html/create_user.html')


@app.before_request
def validate_session_token():
    global email
    # check if the user is authenticated
    if current_user.is_authenticated:
        db_token = Employee.query.filter_by(EmployeeID=current_user.get_id()).first().session_token
        session_token = session.get('user_token')
        # validating the user session token
        if not session_token or session_token != db_token:
            # requiring the user to re-login if user's session token is invalid
            logout_user()
            logger.warning("[!] " + str(email) + "\'s session token is invalid!")
            return redirect('/login')
        logger.info("[*] " + str(email) + "\'s session token is valid")


def create_space_chart(used_space, free_space):
    labels = 'Used Space', 'Free Space'
    sizes = [used_space, free_space]
    colors = ['red', 'green']
    explode = (0.1, 0)  # explode the 1st slice (i.e., 'Used Space')

    plt.figure(figsize=(6, 4))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the plot as a .png file
    plt.savefig('static/inventory_space.png')
    plt.close()


@app.route('/inventory', methods=["GET", "POST"])
@login_required
def inventory():
    items = Inventory.query.all()
    item_in = []
    item_out = []
    for i in range(len(items)):
        if items[i]["Out_Date"] is None:
            item_in.append(items[i])
        else:
            item_out.append(items[i])
    total_items_in = len(items_in)
    total_capacity = 1000
    used_space = sum(item.Quantity for item in items_in)
    free_space = total_capacity - used_space
    # generating the chart that's going to be displayed on the webpage
    create_space_chart(used_space, free_space)
    item_id = request.form.get('item_id')
    action = request.form.get('action')
    submit = request.form.get('submit')
    all_items = Inventory.query.all()
    if item_id:
        if action == 'i_edit':
            return redirect("/edit_item/" + str(item_id))
        elif action == 'i_check_out':
            return check_out_item(item_id)
        elif action == 'o_edit':
            return redirect("/edit_item/" + str(item_id))
        elif action == 'o_del':
            Inventory.query.filter(Inventory.Item_Id == item_id).delete()
            return redirect("/inventory")
        else:
            return redirect("/inventory")
    return render_template('html/inventory.html', items=items_in, o_items=item_out, total_items=total_items_in,
                           available_space=free_space)


def check_out_item(item_id):
    c_item = Inventory.query.get(item_id)
    c_item.OutDate = str(log_name)
    db.session.commit()
    logger.info("[*] Checked out item with ID: " + str(item_id))
    return redirect("/inventory")


@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    e_item = Inventory.query.get(item_id)
    if request.method == 'POST':
        db.session.add(e_item)
        if request.form.get('name'):
            e_item.I_Name = request.form.get('name')
        if request.form.get('disc'):
            e_item.I_Disc = request.form.get('disc')
        if request.form.get('in_date'):
            e_item.InDate = request.form.get('in_date')
        if request.form.get('warehouse_num'):
            e_item.Warehouse_Num = request.form.get('warehouse_num')
        if request.form.get('quantity'):
            e_item.Quantity = request.form.get('quantity')
        db.session.commit()
        return redirect('/inventory')
    return render_template('html/edit_item.html', item=e_item)


@app.route('/check_in_item', methods=['GET', 'POST'])
@login_required
# creating new users
def check_in_item():
    if request.method == 'POST':
        id = request.form.get('ItemId')
        name = request.form.get('i_name')
        disc = request.form.get('i_disc')
        date = str(log_name)
        od = None
        warehouse_num = request.form.get('warehouse_num')
        quantity = request.form.get('quantity')
        new_item = Inventory(ItemID=id, I_Name=name, I_Disc=disc, InDate=date, OutDate=od,
                             Warehouse_Num=warehouse_num,
                             Quantity=quantity)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/inventory')  # Redirect to inventory page
    return render_template('/html/item_in.html')


@app.route("/sales")
@login_required
def sales():
    pass


@app.route("/purchases")
@login_required
def purchases():
    pass


@app.route("/design")
@login_required
def design():
    return render_template("html/design.html")


@app.route('/inventory', methods=["GET", "POST"])
@login_required
def inventory():
    items = Inventory.query.all()
    item_in = []
    item_out = []
    for i in range(len(items)):
        if items[i]["Out_Date"] is None:
            item_in.append(items[i])
        else:
            item_out.append(items[i])
    total_items_in = len(items_in)
    total_capacity = 1000
    used_space = sum(item.Quantity for item in items_in)
    free_space = total_capacity - used_space
    # generating the chart that's going to be displayed on the webpage
    create_space_chart(used_space, free_space)
    item_id = request.form.get('item_id')
    action = request.form.get('action')
    submit = request.form.get('submit')
    all_items = Inventory.query.all()
    if item_id:
        if action == 'i_edit':
            return redirect("/edit_item/" + str(item_id))
        elif action == 'i_check_out':
            return check_out_item(item_id)
        elif action == 'o_edit':
            return redirect("/edit_item/" + str(item_id))
        elif action == 'o_del':
            Inventory.query.filter(Inventory.Item_Id == item_id).delete()
            return redirect("/inventory")
        else:
            return redirect("/inventory")
    return render_template(escape('html/inventory.html'), items=escape(items_in), o_items=item_out,
                           total_items=total_items_in,
                           available_space=free_space)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/design/new_design", methods=["GET", "POST"])
@login_required
def new_design():
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Here you can save `p_name`, `p_detail`, and `filename` to your database if needed
            flash('File successfully uploaded')
            return redirect(url_for('design'))
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template("html/new_design.html")


@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    # global email
    # if request.method == 'POST':
    #     title = request.form['title']
    #     description = request.form['description']
    #     severity = request.form['severity']  # 'info', 'warning', or 'fatal'
    #     # Prepare the card data for Codecks
    #     card_data = {
    #         'content': str(title) + '\n\n' + str(description),
    #         'severity': severity,
    #         "userEmail": str(email)
    #     }
    #
    #     # Codecks API URL and headers
    #     url = 'https://api.codecks.io/user-report/v1/create-report?token=rt_ddrASKCqSAXfN9FJsJwOuU4n'
    #     headers = {
    #         'Content-Type': 'application/json'
    #     }
    #
    #     # Send the request to Codecks
    #     print('sending...')
    #     response = requests.post(url, json=json.dumps(card_data), headers=headers)
    #     print('sent')
    #     print(response)
    #     if response.status_code == 201:
    #         flash('Your request has been submitted successfully!', 'success')
    #         return redirect('/dashboard')
    #     else:
    #         return redirect('/report')

    return render_template('html/report.html')


# data model definition

# model for employees
class Employee(UserMixin, db.Model):
    __tablename__ = 'employee'
    EmployeeID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=True)
    Dept = db.Column(db.String(30), nullable=True)
    Email = db.Column(db.String(30), unique=True, nullable=True)
    Password = db.Column(db.String(90), nullable=True)
    session_token = db.Column(db.String(100), nullable=True)

    def get_id(self):
        return str(self.EmployeeID)


# model for inventory
class Inventory(UserMixin, db.Model):
    __tablename__ = 'inventory'
    ItemID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    I_Name = db.Column(db.String(20), nullable=True)
    I_Disc = db.Column(db.String(500), nullable=True)
    InDate = db.Column(db.String(10), nullable=True)
    OutDate = db.Column(db.String(10), nullable=True)
    Warehouse_Num = db.Column(db.Integer, nullable=True)
    Quantity = db.Column(db.Integer, nullable=True)

    def get_id(self):
        return str(self.EmployeeID)
