from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = ''  # Change this to a secure key

# Database configuration
app.config[''] = ''
app.config[''] = False
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Review model
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# Favorite model
class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant = db.Column(db.String(100), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.date_posted.desc()).all()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', reviews=reviews, favorites=favorites)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Check your username and password.')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/post_review', methods=['GET', 'POST'])
@login_required
def post_review():
    if request.method == 'POST':
        restaurant = request.form['restaurant']
        rating = int(request.form['rating'])
        review = request.form['review']

        new_review = Review(restaurant=restaurant, rating=rating, review=review, user_id=current_user.id)
        db.session.add(new_review)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('post_review.html')

@app.route('/favorite/<restaurant>', methods=['POST'])
@login_required
def favorite(restaurant):
    existing_favorite = Favorite.query.filter_by(user_id=current_user.id, restaurant=restaurant).first()
    if not existing_favorite:
        new_favorite = Favorite(user_id=current_user.id, restaurant=restaurant)
        db.session.add(new_favorite)
        db.session.commit()
        flash(f'{restaurant} added to favorites.')
    else:
        flash(f'{restaurant} is already in your favorites.')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
