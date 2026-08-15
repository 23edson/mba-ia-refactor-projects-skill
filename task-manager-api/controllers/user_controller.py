import re
from database import db
from models.user import User
from models.task import Task

def list_users():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'role': u.role,
            'active': u.active,
            'created_at': str(u.created_at),
            'task_count': len(u.tasks)
        })
    return result

def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError('Usuário não encontrado')

    data = user.to_dict()
    tasks = Task.query.filter_by(user_id=user_id).all()
    data['tasks'] = [t.to_dict() for t in tasks]
    return data

def create_user(name, email, password, role='user'):
    if not name:
        raise ValueError('Nome é obrigatório')
    if not email:
        raise ValueError('Email é obrigatório')
    if not password:
        raise ValueError('Senha é obrigatória')

    if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
        raise ValueError('Email inválido')

    if len(password) < 4:
        raise ValueError('Senha deve ter no mínimo 4 caracteres')

    if role not in ['user', 'admin', 'manager']:
        raise ValueError('Role inválido')

    existing = User.query.filter_by(email=email).first()
    if existing:
        raise ValueError('Email já cadastrado')

    user = User()
    user.name = name
    user.email = email
    user.set_password(password)
    user.role = role

    db.session.add(user)
    db.session.commit()
    return user.to_dict()

def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        raise ValueError('Usuário não encontrado')

    if 'name' in data:
        user.name = data['name']

    if 'email' in data:
        email = data['email']
        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
            raise ValueError('Email inválido')

        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user_id:
            raise ValueError('Email já cadastrado')
        user.email = email

    if 'password' in data:
        password = data['password']
        if len(password) < 4:
            raise ValueError('Senha muito curta')
        user.set_password(password)

    if 'role' in data:
        role = data['role']
        if role not in ['user', 'admin', 'manager']:
            raise ValueError('Role inválido')
        user.role = role

    if 'active' in data:
        user.active = data['active']

    db.session.commit()
    return user.to_dict()

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError('Usuário não encontrado')

    tasks = Task.query.filter_by(user_id=user_id).all()
    for t in tasks:
        db.session.delete(t)

    db.session.delete(user)
    db.session.commit()

def get_user_tasks(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError('Usuário não encontrado')

    tasks = Task.query.filter_by(user_id=user_id).all()
    result = []
    for t in tasks:
        task_data = t.to_dict()
        task_data['overdue'] = t.is_overdue()
        result.append(task_data)
    return result

def login(email, password):
    if not email or not password:
        raise ValueError('Email e senha são obrigatórios')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        raise ValueError('Credenciais inválidas')

    if not user.active:
        raise ValueError('Usuário inativo')

    import jwt
    from datetime import datetime, timedelta
    from flask import current_app

    payload = {
        'sub': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    return {
        'user': user.to_dict(),
        'token': token
    }
