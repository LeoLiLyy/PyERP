from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from . import auth_bp
from ..extensions.official.language_manager import _


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    global user, email
    # the method will change to POST if the login button is pressed
    # detection for the change in method is done here
    if request.method == 'POST':
        # email and password typed in the html form is stored here
        email = request.form['email']
        # password is hashed immediately
        password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        # query for user is done here
        user = Employee.query.filter_by(Email=email, Password=password).first()

        logger.debug("[!] List of users detected:" + str(user))

        if user:
            # requests.post("http://localhost:80/erp_admin_ntfy",
            #               data=str(str(request.form["email"]) + " is now logged in!").encode(encoding='utf-8'))
            logger.info("[*] " + str(request.form["email"]) + " is now logged in!")
            login_user(user, remember=request.form.get('remember', 'false').lower() in ['true', '1', 't'])
            # all users online is stored in this list
            users_online.append(email)
            # the session token (which is stored in the database) is used to verify and kick users that's currently
            # online
            session_token = os.urandom(24).hex()
            # storing the session token in the session (bruh)
            user.session_token = session_token
            db.session.commit()
            session['user_token'] = session_token
            return redirect('/dashboard')
        else:
            logger.warning("Illegal login attempt detected")
            # requests.post("http://localhost:80/erp_admin_ntfy",
            #               data="Illegal login attempt detected".encode(encoding='utf-8'))
            language_manager = LanguageManager('zh_cn')  # Example: dynamically determine the language
            return render_template('login.html', _=_)
    language_manager = LanguageManager('zh_cn')  # Example: dynamically determine the language
    return render_template('login.html', _=_)


@login_required
@auth_bp.route("/logout")
def logout():
    # removing the user from the list of online users
    users_online.remove(email)
    user_fil = Employee.query.filter_by(EmployeeID=current_user.get_id()).first()
    if user_fil:
        # flush the session token as you won't be needing it for a user that's logged out
        user_fil.session_token = None
        db.session.commit()
    session.pop('user_token', None)
    logout_user()
    # requests.post("http://localhost:80/erp_admin_ntfy",
    #               data=str(email) + " is now logged out").encode(encoding='utf-8')
    logger.info("[*] " + str(email) + " is now logged out")
    return redirect("/")
