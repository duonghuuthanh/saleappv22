from flask import render_template, request, redirect, jsonify, session
from saleapp import app, utils, login
from saleapp.admin import *
from saleapp.models import User
from flask_login import login_user
import hashlib, os


@app.route("/")
def index():
    categories = utils.read_data()

    return render_template('index.html',
                           categories=categories)


@app.route('/products')
def product_list():
    cate_id = request.args.get("category_id")
    kw = request.args.get("kw")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    products = utils.read_products(category_id=cate_id,
                                   kw=kw,
                                   from_price=from_price,
                                   to_price=to_price)

    return render_template('products.html', products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = utils.get_product_by_id(product_id=product_id)

    return render_template('product-detail.html',
                           product=product)


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm-password', '').strip()

        if password == confirm:
            f = request.files["avatar"]
            avatar_path = 'images/upload/%s' % f.filename
            f.save(os.path.join(app.config['ROOT_PROJECT_PATH'],
                                'static/', avatar_path))

            if utils.add_user(name=name, username=username, password=password,
                              email=email, avatar=avatar_path):
                return redirect('/')
            else:
                err_msg = "Thêm user có lỗi! Vui long quay lại sau!"
        else:
            err_msg = 'Mật khẩu không khớp!'


    return render_template('register.html', err_msg=err_msg)

@app.route('/login', methods=['post'])
def login_usr():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

        user = User.query.filter(User.username == username,
                                 User.password == password).first()

        if user:
            login_user(user=user)

    return redirect('/admin')


@app.route('/api/cart', methods=['post'])
def cart():
    if 'cart' not in session:
        session['cart'] = {}

    data = request.json
    product_id = str(data.get('id'))
    product_name = data.get('name')
    price = data.get('price', 0)

    cart = session['cart']
    if product_id in cart: # có sản phẩm trong giỏ
        cart[product_id]['quantity'] = cart[product_id]['quantity'] + 1
    else: # chưa có sản phẩm trong giỏ
        cart[product_id] = {
            "product_id": product_id,
            "product_name": product_name,
            "price": price,
            "quantity": 1
        }

    session["cart"] = cart

    total_quantity, total_amount = utils.cart_stats(session['cart'])

    return jsonify({
        'total_quantity': total_quantity,
        'total_amount': total_amount
    })


@app.route('/payment', methods=['get', 'post'])
def payment():
    if request.method == 'POST':
        if utils.add_receipt(session.get('cart')):
            del session['cart']

            return jsonify({'message': "Added receipt successful!!!"})

    quan, amount = utils.cart_stats(session.get('cart'))
    cart_info = {
        'total_quantity': quan,
        'total_amount': amount
    }
    return render_template('payment.html', cart_info=cart_info)


@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)