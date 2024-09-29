from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user, current_user
from app.forms import LoginForm, RegisterForm
from app import db
from app.models import User
import sqlalchemy as sa



auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.Select(User).where(User.username == form.username.data)
        )
        
        if user is None or not user.validate_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user=user)
        flash(f'Welcome {user.username}', 'success')
        
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Login', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def signup():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User has been created successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Signup', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))