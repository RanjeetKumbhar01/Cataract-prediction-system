from firebase_config import initialize_firebase
from firebase_admin import auth, db
from flask import Flask, render_template, request, redirect, url_for, flash, session
import logging ,os


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_key') # Necessary for using flash messages.
initialize_firebase()
# session.clear()
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home(): 
    return render_template('/index.html')

@app.route('/signup_patient', methods=['GET', 'POST'])
def signup_patient():
    if request.method == 'POST':
        # Get form data
        # logging.info(f"Form Data: {request.form}\n")
        name = request.form['name']
        age = request.form['age']
        password = request.form['password']
        email = request.form['email']
        # name = request.form.get('name')
        # password = request.form.get('password')
        # email = request.form.get('email')
        # age = request.form.get('age')
        logging.info(f"Registration data: name={name}, age={age},password={password}, email={email}\n")

        try:
            # Create a new user with Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            logging.info(f"Firebase user created: {user.uid}")
                   # Store additional user info in Firebase Realtime Database
            ref = db.reference(f'p-users/{user.uid}')
            ref.set({
                'name': name,
                'email': email,
                'user_type': 'patient'
            })
            flash(f'Registration successful for {name}!', 'success')

        # except auth.AuthError as e:
        #     logging.error(f"Error creating user: {str(e)}")
        #     if 'WEAK_PASSWORD' in str(e):
        #         flash('Error: Password should be at least 6 characters long.', 'error')
        #     else: 
        #         flash(f'Error: {str(e)}', 'error')

        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            flash(f'Error: {str(e)}', 'error')

        return redirect(url_for('login'))

    return render_template('signup_patient.html')

@app.route('/signup_staff', methods=['GET', 'POST'])
def signup_staff():
    if request.method == 'POST':
        # Get form data
        # logging.info(f"Form Data: {request.form}\n")
        name = request.form['name']
        HospitalName = request.form['HospitalName']        # name = request.form.get('name')
        email = request.form['email']
        password = request.form['password']
        # password = request.form.get('password')
        # email = request.form.get('email')
        # age = request.form.get('age')
        logging.info(f"Registration data: name={name}, HospitalName={HospitalName},password={password}, email={email}\n")

        try:
            # Create a new user with Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            logging.info(f"Firebase user created: {user.uid}")
                   # Store additional user info in Firebase Realtime Database
            ref = db.reference(f's-users/{user.uid}')
            ref.set({
                'name': name,
                'email': email,
                'user_type': 'staff'
            })
            flash(f'Registration successful for {name}!', 'success')

        except auth.AuthError as e:
            logging.error(f"Error creating user: {str(e)}")
            if 'WEAK_PASSWORD' in str(e):
                flash('Error: Password should be at least 6 characters long.', 'error')
            else:
                flash(f'Error: {str(e)}', 'error')

        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            flash(f'Error: {str(e)}', 'error')

        return redirect(url_for('signup_staff'))

    return render_template('signup_staff.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']
        
        logging.info(f"login attempt: , email={email}, password={password}")
        logging.info(f"login attempt: , email={type(email)}, password={type(password)}")

        try:
            user = auth.sign_in_with_email_and_password(email,password)
            logging.info(f"Loggin successfull ",user)
            name = user.display_name

            return redirect(url_for('dashboard', name=name))

        except Exception as e:
            flash("Invalid email or password.", 'error')
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/dashboard')
def dashboard(name):
    return render_template("dashboard.html",name)


@app.route('/logout')
def logout():
    flash("You have been logged out.", 'info')
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)

