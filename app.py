from flask import Flask, request, render_template, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from typing import Callable, Any
from functools import wraps

from config import MONGO_URI, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

client = MongoClient(MONGO_URI)
db = client['luxious']


def login_required(func: Callable) -> Callable:
    @wraps(func)
    def decorated_func(*args, **kwargs) -> Any:
        if 'user_id' not in session:
            flash("You must be logged in to access this page", "warning")
            return redirect(url_for('login', next=request.endpoint))
        return func(*args, **kwargs)
    return decorated_func


@app.route('/')
def home():
    products = list(db.products.find()) 
    return render_template("index.html", products=products)


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password']
        email = request.form['email'].strip()

        if db.users.find_one({"username":username}):
            flash("Username already exists", "danger")
            return redirect(url_for('register'))
        
        if db.users.find_one({"email":email}):
            flash("Email already registered", "danger")
            return redirect(url_for('register'))
        
        password_hash = generate_password_hash(password)
        db.users.insert_one({
            "username":username,
            "password":password_hash,
            "email":email,
        })

        flash("Registration successful! Please login", "success")
        return redirect(url_for('login'))
    
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password']

        user = db.users.find_one({"username":username})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user["_id"])
            session['username'] = user['username']
            flash(f"Welcome, {user['username']}!", "success")
            next_page = request.args.get('next')
            return redirect(url_for(next_page)) if next_page else redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template("login.html")


@app.route('/add_to_cart/<product_id>', methods=["POST"])
@login_required
def add_to_cart(product_id):
    try:
        product = db.products.find_one({'_id': ObjectId(product_id)})
        if product:
            product['_id'] = str(product['_id'])  
            cart = session.get('cart', [])
            cart.append(product)
            session['cart'] = cart
    except Exception as e:
        flash("Invalid product.", "danger")
    return redirect(url_for('home'))

@app.route('/remove_from_cart/<product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    updated_cart = [item for item in cart if item['_id'] != product_id]
    session['cart'] = updated_cart
    # flash("Item removed from cart.", "info")
    return redirect(url_for('cart'))


@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html', cart=session.get('cart', []))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        session.pop('cart', None)
        return render_template('checkout_success.html')
    return render_template('checkout.html', cart=session.get('cart', []))

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
