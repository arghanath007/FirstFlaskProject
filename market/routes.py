from market import app
from flask import render_template,redirect,url_for,flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm,SellItemForm
from market import db
from flask_login import login_user,logout_user, login_required, current_user


@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form=PurchaseItemForm()
    selling_form= SellItemForm()
    if request.method == 'POST':


        # Purchasing an item from the market logic
        purchased_item= request.form.get('purchased_item')
        purchased_item_object= Item.query.filter_by(name=purchased_item).first()
        if purchased_item_object:
            if current_user.can_purchase(purchased_item_object):
                purchased_item_object.buy(current_user)
                flash(f'Congratulation!!, your purchase of {purchased_item_object.name} was successfully for {purchased_item_object.price}$ ',  category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {purchased_item_object.name} from the market", category='danger')

        # Selling an item to the market from the user owned items logic
        sold_item=request.form.get('sold_item')
        sold_item_object= Item.query.filter_by(name=sold_item).first()
        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                sold_item_object.sell(current_user)
                flash(f'Congratulation!!, your have successfully sold {sold_item_object.name} back to the market',  category='success')
            else:
                flash(f"Something went wrong unfortunately during the selling of {sold_item_object.name} to the market", category='danger')   

        return redirect(url_for('market_page'))

    if request.method == 'GET':
                            # if purchase_form.validate_on_submit():
                            # print(purchase_form.__dict__)
                            # print(purchase_form['submit'])
                            # print(request.form.get('purchased_item'))
        items = Item.query.filter_by(owner=None)
        owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items,purchase_form=purchase_form,owned_items=owned_items, selling_form=selling_form)
    

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form= RegisterForm()
    if form.validate_on_submit(): # 1)Checks if the user has    clicked on the submit button. 2) Write some validations that are going to check for some requirements before the form becomes valid.
        user_to_create= User(username=form.username.data, email=form.email.data, password=form.password.data)

        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Accounted created successfully, You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are no errors from the validations in the form
        for error_message in form.errors.values():
            flash(f'There was an error with creating a user:{error_message}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success!! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
    else:
        flash('Username and password does not match!!! Try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been successfully logged", category='info')
    return redirect(url_for('home_page'))

