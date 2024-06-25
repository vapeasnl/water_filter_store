from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import app, db
from app.models import Product, Review
from app.forms import ReviewForm

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()
    form = ReviewForm()
    return render_template('product.html', product=product, reviews=reviews, form=form)

@app.route('/product/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(body=form.body.data, author=current_user, product_id=product_id)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been added.')
    return redirect(url_for('product', product_id=product_id))
