import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length, EqualTo
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Set up SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    reviews = relationship("Review", back_populates="user")

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False)
    address = Column(String(300), nullable=False)
    reviews = relationship("Review", back_populates="restaurant", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Integer, nullable=False)
    text_review = Column(Text, nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    restaurant = relationship("Restaurant", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

Base.metadata.create_all(bind=engine)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == int(user_id)).first()
    db.close()
    return user

# Forms
class AddRestaurantForm(FlaskForm):
    name = StringField('Restaurant Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Add Restaurant')

class AddReviewForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    text_review = TextAreaField('Optional Text Review')
    submit = SubmitField('Add Review')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
def index():
    # Show all restaurants
    db = SessionLocal()
    restaurants = db.query(Restaurant).all()
    db.close()
    return render_template('index.html', restaurants=restaurants)

@app.route('/add_restaurant', methods=['GET', 'POST'])
@login_required
def add_restaurant():
    form = AddRestaurantForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        address = form.address.data.strip()
        db = SessionLocal()
        new_restaurant = Restaurant(name=name, address=address)
        db.add(new_restaurant)
        try:
            db.commit()
            flash("Restaurant added successfully!", "success")
        except IntegrityError:
            db.rollback()
            flash("A restaurant with that name already exists.", "danger")
        db.close()
        return redirect(url_for('index'))
    return render_template('add_restaurant.html', form=form)

@app.route('/restaurant/<int:restaurant_id>')
def restaurant_detail(restaurant_id):
    db = SessionLocal()
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        db.close()
        return "Restaurant not found", 404
    reviews = restaurant.reviews
    db.close()
    return render_template('restaurant_detail.html', restaurant=restaurant, reviews=reviews)

@app.route('/restaurant/<int:restaurant_id>/add_review', methods=['GET', 'POST'])
@login_required
def add_review(restaurant_id):
    form = AddReviewForm()
    db = SessionLocal()
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        db.close()
        return "Restaurant not found", 404

    if form.validate_on_submit():
        rating = form.rating.data
        text_review = form.text_review.data.strip() if form.text_review.data else None
        new_review = Review(rating=rating, text_review=text_review, restaurant=restaurant, user=current_user)
        db.add(new_review)
        db.commit()
        db.close()
        flash("Review added successfully!", "success")
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    db.close()
    return render_template('add_review.html', form=form, restaurant=restaurant)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        db = SessionLocal()
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            db.close()
            flash("Username already exists.", "danger")
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)
        new_user = User(username=username, password_hash=password_hash)
        db.add(new_user)
        db.commit()
        db.close()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            db.close()
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))
        db.close()
        flash("Invalid username or password.", "danger")

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
