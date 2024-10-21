# from firebase_config import initialize_firebase
# from firebase_admin import auth, db
from flask import Flask, render_template, request, redirect, url_for, flash, session
import logging 
import mysql.connector
from mysql.connector import IntegrityError 
import bcrypt
import re  
app = Flask(__name__)
app.secret_key = "key"
# initialize_firebase()


# MySQL connection configuration
conn = mysql.connector.connect(
    host="localhost",  # or your MySQL server
    user="root",
    password="root",
    database="user_management"  # The name of your MySQL database
)
cursor = conn.cursor()

logging.basicConfig(level=logging.INFO)



# Helper function to validate email
def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)

# Helper function to validate password
def is_valid_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if len(password) > 32:
        return False, "Password must not exceed 32 characters."
    return True, ""

def is_valid_age(age):
    if int(age) < 10 or int(age) > 100:
        return False, "Please enter a valid age between 10 and 100."
    return True,""

def is_valid_name(name):
    if re.match("^[A-Za-z ]{2,}$", name):
        return True
    else:
        return False

@app.route('/')
def home(): 
    return render_template('/index.html')

@app.route('/signup_patient', methods=['GET', 'POST'])
def signup_patient():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        age = request.form['age']
        password = request.form['password']
        email = request.form['email']
        logging.info(f"Registration data: name={name}, age={age},password={password}, email={email}\n")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Validate name
        if not is_valid_name(name):
            flash("Invalid name format.")
            return redirect(url_for('signup_patient'))
        
        # Validate email
        if not is_valid_email(email):
            flash("Invalid email format. Please use a valid email like 'user@example.com'.")
            return redirect(url_for('signup_patient'))

        valid_password, password_msg = is_valid_password(password)
        if not valid_password:
            flash(password_msg)
            return redirect(url_for('signup_patient'))

        valid_age, age_msg = is_valid_age(age)
        if not valid_age:
            flash(age_msg)
            return redirect(url_for('signup_patient'))
        

        try:
            sql = "INSERT INTO users (name, email, password, age, user_type) VALUES (%s, %s, %s, %s,'patient')"
            cursor.execute(sql, (name, email, hashed_password, age))
            conn.commit()
            flash(f'Registration successful for {name}!')
        
        except IntegrityError as e:  # Catch duplicate email errors
            if e.errno == 1062:  # 1062 is the error code for duplicate entry in MySQL
                flash("This email is already registered. Please use a different email.", 'error')
            else:
                flash(f'Error: {str(e)}', 'error')

            return redirect(url_for('signup_patient'))
            
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('signup_patient'))

        return redirect(url_for('login'))

    return render_template('signup_patient.html')

@app.route('/signup_staff', methods=['GET', 'POST'])
def signup_staff():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        HospitalName = request.form['HospitalName']        # name = request.form.get('name')
        email = request.form['email']
        password = request.form['password']
        logging.info(f"Registration data: name={name}, HospitalName={HospitalName},password={password}, email={email}\n")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


        # Validate name
        if not is_valid_name(name):
            flash("Invalid name format.")
            return redirect(url_for('signup_staff'))
        
        if not is_valid_name(HospitalName):
            flash("Invalid Hospital Name.")
            return redirect(url_for('signup_staff'))
        
        # Validate email
        if not is_valid_email(email):
            flash("Invalid email format. Please use a valid email like 'user@example.com'.")
            return redirect(url_for('signup_staff'))

        valid_password, password_msg = is_valid_password(password)
        if not valid_password:
            flash(password_msg)
            return redirect(url_for('signup_staff'))

        try:
            # Insert the data into the MySQL database
            sql = "INSERT INTO users (name, email, password, user_type, hospital_name) VALUES (%s, %s, %s, 'staff', %s)"
            cursor.execute(sql, (name, email, hashed_password, HospitalName))
            conn.commit()
            flash(f'Registration successful for {name}!')

        except IntegrityError as e:  # Catch duplicate email errors
            if e.errno == 1062:  # 1062 is the error code for duplicate entry in MySQL
                flash("This email is already registered. Please use a different email.", 'error')
            else:
                flash(f'Error: {str(e)}', 'error')

            return redirect(url_for('signup_staff'))

        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            flash(f'Error: {str(e)}', 'error')

        return redirect(url_for('login'))

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
            # user = auth.sign_in_with_email_and_password(email,password)
            # name = user.display_name
                    # Fetch the user's password from the MySQL database
            sql = "SELECT name, password FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            if result:
                stored_name, stored_password = result

            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                      logging.info(f"Loggin successfull ",stored_name)
            else:
                logging.info(f"Invalid password ",stored_name)
                flash("Invalid email or password.")
                return redirect(url_for("login"))

            return redirect(url_for('dashboard', name=stored_name))

        except Exception as e:
            flash("Invalid email or password.", 'error')
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/dashboard/<name>')
def dashboard(name):
    return render_template("dashboard.html",name=name)


@app.route('/logout')
def logout():
    flash("You have been logged out.", 'info')
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)

