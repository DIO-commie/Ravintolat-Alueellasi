from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Replace these with your PostgreSQL database credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/restaurant_reviews'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a Review model
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, restaurant, rating, review):
        self.restaurant = restaurant
        self.rating = rating
        self.review = review

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    reviews = Review.query.order_by(Review.date_posted.desc()).all()
    return render_template('index.html', reviews=reviews)

@app.route('/post_review', methods=['GET', 'POST'])
def post_review():
    if request.method == 'POST':
        restaurant = request.form['restaurant']
        rating = int(request.form['rating'])
        review = request.form['review']

        new_review = Review(restaurant=restaurant, rating=rating, review=review)
        db.session.add(new_review)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('post_review.html')

if __name__ == '__main__':
    app.run(debug=True)
