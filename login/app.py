from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import User
from snowflake.connector import connect  # Import for connection

from config import SECRET_KEY, SNOWFLAKE  # Import configuration

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SNOWFLAKE'] = SNOWFLAKE

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Set login view route

@login_manager.user_loader
def load_user(email):
    return User.get_by_email() 

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']  # Assuming username is still collected for display
        email = request.form['email']
        password = request.form['password']
        city = request.form['city'] if 'city' in request.form else None

        try:
            # Validate unique email (assuming no password hashing)
            if User.get_by_email(email):
                flash('Email address already exists. Please choose another one.', 'danger')
                return render_template('signup.html')

            # Insert user data without password hashing (not recommended in production)
            if User.create_user(username, email, password, city):
                flash('Registration Successful (without password hashing - not recommended)!', 'warning')
                return redirect(url_for('login'))
            else:
                flash(f'An unexpected error occurred. Please try again later.', 'danger')
        except Exception as e:
            print(f'Error creating user: {str(e)}')  # Log the error for troubleshooting
            flash(f'An unexpected error occurred. Please try again later.', 'danger')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_active:  # Check for activeness before redirecting
        return redirect(url_for('product')) 
    # ... rest of the login function ...

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.get_by_email(email)  # Retrieve user by email

        if user and password == user.password :  # Use a secure verification method
            login_user(user)
            return redirect(url_for('product'))  # Redirect to product page
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


# You'll need to create the 'home' route and any other protected routes
# Remember to create the signup.html and login.html templates (see below)

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
