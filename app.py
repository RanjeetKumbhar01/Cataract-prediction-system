from firebase_config import initialize_firebase
from firebase_admin import auth
from flask import Flask, render_template, request, redirect, url_for, flash
import logging ,os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_key') # Necessary for using flash messages.
initialize_firebase()


logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        logging.info(f"Registration data: username={username}, password={password}, email={email}")

        try:
                    # Create a new user with Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password,
                display_name=username
            )
            logging.info(f"Firebase user created: {user.uid}")

            flash(f'Registration successful for {username}!', 'success')
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            flash(f'Error: {str(e)}', 'error')

        return redirect(url_for('register'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
