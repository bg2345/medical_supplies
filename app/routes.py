from app import app, db
from flask import render_template, url_for, redirect, flash, request
from app.forms import TitleForm, PostForm, LoginForm, RegisterForm, ContactForm
from app.models import Post, User
from flask_login import current_user, login_user, logout_user, login_required
import stripe
from app.email import send_email

stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.route('/')
@app.route('/index')
@app.route('/index/<header>', methods=['GET'])
def index(header=''):
    products = [
        {
            'id': 1001,
            'title': 'Sterile Alchohol Prep Pads',
            'price': 12.98,
            'desc': 'Box of 100 pads. Sterile, 70% alcohol.',
            'image': 'https://cdn.shopify.com/s/files/1/0021/5692/0919/products/71bEP-EAxvL._SL1500_720x.jpg?v=1584548531'
        },
        {
            'id': 1002,
            'title': 'Latex Medical Gloves',
            'price': 15.56,
            'desc': 'Box of 100 medical gloves, size Large.',
            'image': 'http://placehold.it/250x250'
        },
        {
            'id': 1003,
            'title': 'Surgical Masks',
            'price': 15.67,
            'desc': 'Package of 2 surgical masks.',
            'image': 'http://placehold.it/250x250'
        },
        {
            'id': 1004,
            'title': 'Syringes',
            'price': 22.68,
            'desc': 'Box of 100 syringes.',
            'image': 'http://placehold.it/250x250'
        }
    ]


    return render_template('index.html', header=header, products=products, title='Home')

@login_required
@app.route('/posts/<username>', methods=['GET', 'POST'])
def posts(username):
    form = PostForm()

    # query db for proper person
    person = User.query.filter_by(username=username).first()

    # when form is submitted append to posts list, re-render posts page
    if form.validate_on_submit():
        tweet = form.tweet.data
        post = Post(tweet=tweet, user_id=current_user.id)

        # add post variable to database stage, then commit
        db.session.add(post)
        db.session.commit()

        # reloads page
        return redirect(url_for('posts', username=username))

    return render_template('posts.html', person=person, title='Posts', form=form, username=username)


@app.route('/title', methods=['GET', 'POST'])
def title():
    form = TitleForm()

    # when form is submitted, redirect to home page, and pass title to change what the h1 tag says
    if form.validate_on_submit():
        header = form.title.data
        return redirect(url_for('index', header=header))

    return render_template('title.html', title='Title', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # if user is logged in already, do not let them access this page
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data,
            url = form.url.data,
            age = int(form.age.data),
            bio = form.bio.data
        )

        # set password hash
        user.set_password(form.password.data)

        # add to stage and commit to db, then flash and return
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('index'))

    form = LoginForm()

    # check if form is submitted, Log user in if so
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        #if user doesn't exist, reload page and flash message
        if user is None or not user.check_password(form.password.data):
            flash('Credentials are incorrect.')
            return redirect(url_for('login'))

        # if user does exist, and credentials are correct, log thm in and send them to their profile page
        login_user(user, remember=form.remember_me.data)
        flash('You are now logged in!')
        return redirect(url_for('posts', username=current_user.username))


    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    return render_template('checkout.html', title='Checkout')

@app.route('/pay/', methods=['GET', 'POST'])
def pay():

    amount = request.args.get('amount')

    email = request.form['stripeEmail']

    customer = stripe.Customer.create(
        email=email,
        source=request.form['stripeToken']
    )

    # create a stripe charge
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='This was a test purchase for some test products'
    )


    return redirect(url_for('thanks', amount=amount, email=email))

@app.route('/thanks/<amount>/<email>', methods=['GET'])
def thanks(amount, email):
    # convert amount back to dollars
    amount = int(amount) / 100

    return render_template('thanks.html', amount=amount, email=email, title='Thanks')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        send_email(
        subject = 'Contact Form',
        sender = app.config['ADMINS'][0],
        recipients = [form.email.data],
        text_body = render_template('email/contact_form.txt',
            name = form.name.data,
            message = form.message.data),
        html_body = render_template('email/contact_form.html',
            name = form.name.data,
            message = form.message.data)
    )

        flash('Your email has been sent.')
        return redirect(url_for('index'))


    return render_template('contact.html', form=form, title='Contact')
