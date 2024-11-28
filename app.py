from flask import Flask, render_template, request, redirect, url_for, flash, session
import logging 
import mysql.connector
from mysql.connector import IntegrityError 
import bcrypt
import re  
import os
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import get_custom_objects
from tensorflow.keras import backend as Kbackend
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dropout

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
app = Flask(__name__)
app.secret_key = "key"

# MySQL connection configuration
conn = mysql.connector.connect(
    host="localhost",  # or your MySQL server
    user="root",
    password="root",
    database="user_management"  # The name of your MySQL database
)
cursor = conn.cursor()

# Folder to save uploaded images
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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
    if int(age) < 18 or int(age) > 126:
        return False, "Please enter a valid age between 18 and 125."
    return True,""

def is_valid_name(name):
    # Check if input is empty or contains only whitespace
    if not name.strip():
        print("Warning: Name cannot be empty or consist only of spaces.")
        return False
    
    # Clean up input by removing extra spaces
    name = re.sub(' +', ' ', name.strip())
    
    # Validate cleaned name
    if re.match("^[A-Za-z]+( [A-Za-z]+)*$", name):
        return True
    else:
        print("Warning: Name can only contain letters and single spaces between words.")
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
            # return redirect(url_for('signup_patient'))
            return render_template('signup_patient.html', name=name, age=age, email=email)

        
        # Validate email
        if not is_valid_email(email):
            flash("Invalid email format. Please use a valid email like 'user@example.com'.")
            # return redirect(url_for('signup_patient'))
            return render_template('signup_patient.html', name=name, age=age, email=email)

        valid_password, password_msg = is_valid_password(password)
        if not valid_password:
            flash(password_msg)
            # return redirect(url_for('signup_patient'))
            return render_template('signup_patient.html', name=name, age=age, email=email)

        valid_age, age_msg = is_valid_age(age)
        if not valid_age:
            flash(age_msg)
            # return redirect(url_for('signup_patient'))
            return render_template('signup_patient.html', name=name, age=age, email=email)
        

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
            # return redirect(url_for('signup_staff'))
            # return render_template('signup_staff.html', name=name, email=email)
            return render_template('signup_staff.html', name=name, email=email, HospitalName=HospitalName)

        if not is_valid_name(HospitalName):
            flash("Invalid Hospital Name.")
            # return redirect(url_for('signup_staff'))
            return render_template('signup_staff.html', name=name, email=email, HospitalName=HospitalName)

        # Validate email
        if not is_valid_email(email):
            flash("Invalid email format. Please use a valid email like 'user@example.com'.")
            # return redirect(url_for('signup_staff'))
            return render_template('signup_staff.html', name=name, email=email, HospitalName=HospitalName)
        
        valid_password, password_msg = is_valid_password(password)
        if not valid_password:
            flash(password_msg)
            # return redirect(url_for('signup_staff'))
            return render_template('signup_staff.html', name=name, email=email, HospitalName=HospitalName)
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
    result = request.args.get('result')
    return render_template("dashboard.html", name=name, result=result)

#  Model utilities and helper functions
class Mish(tf.keras.layers.Layer):

    def __init__(self, **kwargs):
        super(Mish, self).__init__(**kwargs)
        self.supports_masking = True

    def call(self, inputs):
        return inputs * Kbackend.tanh(Kbackend.softplus(inputs))

    def get_config(self):
        base_config = super(Mish, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def compute_output_shape(self, input_shape):
        return input_shape
def mish(x):
    return tf.keras.layers.Lambda(lambda x: x*Kbackend.tanh(Kbackend.softplus(x)))(x)

def swish(x):
    return tf.nn.swish(x)

# Define the custom FixedDropout layer if not already defined
#  Model utilities and helper functions
class FixedDropout(Dropout):
    def __init__(self, rate, **kwargs):
        super(FixedDropout, self).__init__(rate, **kwargs)

    def get_config(self):
        config = super(FixedDropout, self).get_config()
        return config


# Ensure the FixedDropout class is defined
def get_custom_objects():
    return {"FixedDropout": FixedDropout}

def load_model_from_path(model_path):
    global model
    custom_objects = {"FixedDropout": FixedDropout, "swish": tf.keras.activations.swish}
    with tf.keras.utils.custom_object_scope(custom_objects):
        model = tf.keras.models.load_model(model_path)
    return model

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define image dimensions
IMG_HEIGHT = 192
IMG_WIDTH = 256
# Function to preprocess image
def preprocess_image(image_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, (IMG_HEIGHT, IMG_WIDTH))
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.expand_dims(img, axis=0)  # Add batch dimension
    return img

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the POST request has a file
    if 'image' not in request.files:
        flash("No file part in the request.", 'error')
        return redirect(request.referrer)

    file = request.files['image']
    
    if file.filename == '':
        flash("No selected file.", 'error')
        return redirect(request.referrer)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print("filename", filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # print("file_path", file_path)
        file_path = file_path.replace('\\', '/')  # Add this line
        # print("updated_file_path", file_path)
        custom_image = preprocess_image(file_path)
        if model is None:
            print("Model failed to load. Please check the file path and custom objects.")
        else:
            print("Model loaded successfully.")

        prediction = model.predict(custom_image)

        prediction_class = np.argmax(prediction, axis=1)

        # Print prediction result
        # print("Predicted Class:", prediction_class)
        if prediction_class == 0:
            result ="Cataract: Not Present"
        elif prediction_class == 1:
            result ="Cataract: Present" 
        # Pass the result to the dashboard or another template
        # flash(f"Analysis Complete: {result}", 'info')
        return render_template('dashboard.html', name=session.get('name', 'User'), result=result)
    else:
        flash("Invalid file type. Please upload a PNG or JPG image.", 'error')
        return redirect(request.referrer)

@app.route('/logout')
def logout():
    flash("You have been logged out.", 'info')
    return redirect(url_for("login"))


if __name__ == '__main__':
    # TF_ENABLE_ONEDNN_OPTS=0
    load_model_from_path("model/efficientnet_b0_model.h5")
    app.run(debug=True)
