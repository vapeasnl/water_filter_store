from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User, Product, Review, Order, Message
from app.forms import LoginForm, RegistrationForm, ReviewForm, MessageForm, ProductForm
from app.decorators import admin_required, user_required

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()
    form = ReviewForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        review = Review(body=form.body.data, author=current_user, product=product)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been submitted.')
        return redirect(url_for('product', product_id=product_id))
    return render_template('product.html', product=product, reviews=reviews, form=form)

@app.route('/message', methods=['GET', 'POST'])
def message():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(name=form.name.data, email=form.email.data, body=form.body.data)
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('index'))
    return render_template('message.html', form=form)

@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/products')
@admin_required
def admin_products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data, price=form.price.data, stock=form.stock.data, image_url=form.image_url.data)
        db.session.add(product)
        db.session.commit()
        flash('Product has been added.')
        return redirect(url_for('admin_products'))
    return render_template('admin/add_product.html', form=form)

@app.route('/admin/messages')
@admin_required
def admin_messages():
    messages = Message.query.all()
    return render_template('admin/messages.html', messages=messages)

@app.route('/profile')
@login_required
def profile():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', orders=orders)
