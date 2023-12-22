from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm , ItemAdd
from market import db
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
@login_required
def market_page():
    page = request.args.get('page', 1, type=int)
    item_per_page = 6
    pagination = Item.query.paginate(page=page,per_page=item_per_page)
    items = pagination.items
    return render_template('market.html', items=items, pagination=pagination)

@app.route('/categories')
def categories():
    return render_template('Categories.html')

@app.route('/description/<int:product_id>')
def description(product_id):
    product = Item.query.get_or_404(product_id)
    return render_template('description.html', product=product)

@app.route('/forgetpassword')
def forget_password():
    return render_template('forgetpassword.html')

#userprofile
#email verificaation page
#review add page
#about us
#contact us page
#product search page

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)  
        flash(f'Account created successfully! you are now logged in as  {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating your account: {err_msg}',category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)  
            flash(f'Success! You are logged in as:  {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password does not exist', category='danger')

    return render_template("login.html", form=form)
    
@app.route('/logout')
def logout_page():
    logout_user()
    flash("you have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/item_add', methods=['GET', 'POST'])
@login_required
def Item_add():
    form = ItemAdd()

    if form.validate_on_submit():
        file = form.image.data
        file.save('market/static/uploads/'+file.filename)
        item_to_add = Item(name=form.title.data,
                           price=form.price.data,
                           description=form.description.data,
                           image=file.filename)

     
        db.session.add(item_to_add)
        db.session.commit()
        flash(f'Item added with item id :{item_to_add.id}', category='success')

        return redirect(url_for('market_page'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with adding the item: {err_msg}',category='danger')
        
    return render_template('itemadd.html', form=form)
