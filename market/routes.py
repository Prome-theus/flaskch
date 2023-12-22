from market import app
from flask import render_template, redirect, url_for, flash, current_user
from market.models import Item, User
from market.forms import RegisterForm, LoginForm , ItemAdd
from flask_oauthlib.client import OAuth
from market import db
from flask_login import login_user, logout_user, login_required


oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='1094737348611-ql5ga54uf68h1bkhf6mulbhvomemsg13.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    redirect_uri='http://localhost:5000/login/authorized/google',
)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
@login_required
def market_page():
    page = request.args.get('page', 1, type=int)
    item_per_page = 6
    pagination = Item.query.paginate(per_page=item_per_page)
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
    if current_user.is_authenticated:
        flash('you are already logged in', 'info')
        return redirect(url_for('home_page'))

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

@app.route('login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        flash('Access denied: Reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('home_page'))
    
    access_token = response['access_token']
    user_info = google.get('userinfo')

    if current_user.is_authenticated:
        current_user.google_id = user_info.data['id']
        db.session.commit()
        flash('successful Linked google account to your profile', 'success')
        return redirect(url_for('home_page'))
    else:
        user = User.query.filter_by(google_id=user_info.data[id]).first()
        if user:
            login_user(user)
            flash(f'Success! you are logged in as: {user.username}', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('google account not linked to any existing user', 'danger')
            return redirect(url_for('home_page'))
    
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

