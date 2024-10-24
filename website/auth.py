
from flask_socketio import SocketIO

from flask import session, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, current_user, LoginManager, logout_user


from .models import User, Server, Channel
from sqlalchemy import func, or_
from . import db

from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/logout')
@login_required
async def logout():
    logout_user()
    return redirect(url_for('views.login'))

@auth.route('/create_acc', methods=['GET', 'POST'])
async def create_acc():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        birth_day = request.form.get('birth_day')
        birth_month = request.form.get('birth_month')
        birth_year = request.form.get('birth_year')

        is_has = User.query.filter(or_(User.email == email, User.name == name)).first()

        if not is_has:
            month_number = {
                'Январь': '01',
                'Февраль': '02',
                'Март': '03',
                'Апрель': '04',
                'Май': '05',
                'Июнь': '06',
                'Июль': '07',
                'Август': '08',
                'Сентябрь': '09',
                'Октябрь': '10',
                'Ноябрь': '11',
                'Декабрь': '12'
            }

            birth_month_numb = month_number.get(birth_month)
            
            if birth_day and birth_month_numb and birth_year:
                birthday = f'{birth_day}.{birth_month_numb}.{birth_year}'
            else:
                return "Некорректная дата рождения", 400 

            new_user = User(
            email = email,
            name = name,
            password = generate_password_hash(password),
            birthday = birthday
            )
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('views.login'))

@auth.route('/sign_in', methods=['GET', 'POST'])
async def sign_in():
    if request.method == 'POST':
        email_telephone = request.form.get('email_telephone')
        password = str(request.form.get('password'))
        user = User.query.filter(or_(func.lower(User.email) == func.lower(email_telephone), User.telephone == email_telephone)).first()
    
        if user:
            session['user_id'] = user.id
            if check_password_hash(user.password, password):
                login_user(user) 
                return redirect(url_for('views.me', user = current_user))
            else:
                return 'Не правильный пароль'
        else:
            return 'Почта/телефон либо пароль указаны с ошибкой'
        

def add_member_to_server(user_id, server_id):
    user = User.query.get(user_id)
    server = Server.query.get(server_id)
    if user and server:
        if user not in server.members:
            server.members.append(user)  
            db.session.commit()

@auth.route('/create_server', methods = ['POST'])
async def create_server():
    if request.method == 'POST':
        name = request.form.get('name')
        new_server = Server(
            name = name, 
            owner_id = current_user.id
        )
        db.session.add(new_server)
        db.session.commit()
        
        add_member_to_server(current_user.id, new_server.id)
        add_member_to_server(current_user.id  + 1, new_server.id)

        new_channel1 = Channel(
            name = 'Текстовый чат №1', 
            is_text = True,
            server_id = new_server.id
        )
        db.session.add(new_channel1)
        new_channel2 = Channel(
            name = 'Голосовой чат №1', 
            is_voice = True,
            server_id = new_server.id
        )
        db.session.add(new_channel2)
        new_channel3 = Channel(
            name = 'Голосовой чат №2', 
            is_voice = True,
            server_id = new_server.id
        )
        db.session.add(new_channel3)
        db.session.commit()

        return redirect(url_for('views.me', user = current_user))
