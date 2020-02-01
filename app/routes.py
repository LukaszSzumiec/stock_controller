from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm
from app.models import User
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from app import db
from .forms import CompanyForm
from .models.model import Company, check_company_if_company_exists
import mpld3
import yfinance as yf
from .utils import open_stock_plot


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = CompanyForm()
    if form.validate_on_submit():
        if not check_company_if_company_exists(form.company.data):
            return redirect(url_for('index'))
        company = Company(body=form.company.data, user=current_user)
        db.session.add(company)
        db.session.commit()
        flash('Added company!')
        return redirect(url_for('index'))
    companies = current_user.followed_companies()
    return render_template("index.html", title='Home Page', form=form, companies=companies)


@app.route("/stocklist", methods=["GET"])
@login_required
def display_stock_list():
    companies = current_user.followed_companies()
    return render_template("stocklist.html", title='Stock list', companies=companies)


@app.route("/stock/<stock_id>", methods=["GET"])
@login_required
def display_plot(stock_id):
    stock = Company.query.get(stock_id)
    if stock is None:
        return jsonify(
            status='error', message='no company with id {}'.format(stock_id))
    open_stock_plot(stock.body)
    return jsonify(status='ok')


@app.route('/stocklist/<stock_id>/delete', methods=['DELETE'])
@login_required
def delete_stock(stock_id):
    stock = Company.query.get(stock_id)
    if stock is None:
        return jsonify(
            status='error', message='no company with id {}'.format(stock_id))
    db.session.delete(stock)
    db.session.commit()
    return jsonify(status='ok')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))