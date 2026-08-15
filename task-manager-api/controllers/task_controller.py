from datetime import datetime
from sqlalchemy.orm import joinedload
from database import db
from models.task import Task
from models.user import User
from models.category import Category

def list_tasks():
    # Eager loading do User e Category para resolver N+1 queries (Finding M-1 / AP-08)
    tasks = Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()
    result = []
    for t in tasks:
        task_data = {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'status': t.status,
            'priority': t.priority,
            'user_id': t.user_id,
            'category_id': t.category_id,
            'created_at': str(t.created_at),
            'updated_at': str(t.updated_at),
            'due_date': str(t.due_date) if t.due_date else None,
            'tags': t.tags.split(',') if t.tags else [],
            'overdue': t.is_overdue(),
            'user_name': t.user.name if t.user else None,
            'category_name': t.category.name if t.category else None
        }
        result.append(task_data)
    return result

def get_task_by_id(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        raise ValueError('Task não encontrada')
    
    data = task.to_dict()
    data['overdue'] = task.is_overdue()
    return data

def create_task(data):
    if not data:
        raise ValueError('Dados inválidos')

    title = data.get('title')
    if not title:
        raise ValueError('Título é obrigatório')
    if len(title) < 3:
        raise ValueError('Título muito curto')
    if len(title) > 200:
        raise ValueError('Título muito longo')

    task = Task()
    
    status = data.get('status', 'pending')
    if not task.validate_status(status):
        raise ValueError('Status inválido')

    priority = data.get('priority', 3)
    try:
        priority = int(priority)
    except (ValueError, TypeError):
        raise ValueError('Prioridade inválida')
    if not task.validate_priority(priority):
        raise ValueError('Prioridade deve ser entre 1 e 5')

    user_id = data.get('user_id')
    if user_id:
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError('Usuário não encontrado')

    category_id = data.get('category_id')
    if category_id:
        cat = db.session.get(Category, category_id)
        if not cat:
            raise ValueError('Categoria não encontrada')

    task.title = title
    task.description = data.get('description', '')
    task.status = status
    task.priority = priority
    task.user_id = user_id
    task.category_id = category_id

    due_date = data.get('due_date')
    if due_date:
        try:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            raise ValueError('Formato de data inválido. Use YYYY-MM-DD')

    tags = data.get('tags')
    if tags:
        if isinstance(tags, list):
            task.tags = ','.join(tags)
        else:
            task.tags = tags

    db.session.add(task)
    db.session.commit()
    return task.to_dict()

def update_task(task_id, data):
    task = db.session.get(Task, task_id)
    if not task:
        raise ValueError('Task não encontrada')

    if not data:
        raise ValueError('Dados inválidos')

    if 'title' in data:
        title = data['title']
        if len(title) < 3:
            raise ValueError('Título muito curto')
        if len(title) > 200:
            raise ValueError('Título muito longo')
        task.title = title

    if 'description' in data:
        task.description = data['description']

    if 'status' in data:
        status = data['status']
        if not task.validate_status(status):
            raise ValueError('Status inválido')
        task.status = status

    if 'priority' in data:
        priority = data['priority']
        try:
            priority = int(priority)
        except (ValueError, TypeError):
            raise ValueError('Prioridade inválida')
        if not task.validate_priority(priority):
            raise ValueError('Prioridade deve ser entre 1 e 5')
        task.priority = priority

    if 'user_id' in data:
        user_id = data['user_id']
        if user_id:
            user = db.session.get(User, user_id)
            if not user:
                raise ValueError('Usuário não encontrado')
        task.user_id = user_id

    if 'category_id' in data:
        category_id = data['category_id']
        if category_id:
            cat = db.session.get(Category, category_id)
            if not cat:
                raise ValueError('Categoria não encontrada')
        task.category_id = category_id

    if 'due_date' in data:
        due_date = data['due_date']
        if due_date:
            try:
                task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except (ValueError, TypeError):
                raise ValueError('Formato de data inválido. Use YYYY-MM-DD')
        else:
            task.due_date = None

    if 'tags' in data:
        tags = data['tags']
        if isinstance(tags, list):
            task.tags = ','.join(tags)
        else:
            task.tags = tags

    task.updated_at = datetime.utcnow()
    db.session.commit()
    return task.to_dict()

def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        raise ValueError('Task não encontrada')
    db.session.delete(task)
    db.session.commit()

def search_tasks(query, status, priority, user_id):
    tasks = Task.query

    if query:
        tasks = tasks.filter(
            db.or_(
                Task.title.like(f'%{query}%'),
                Task.description.like(f'%{query}%')
            )
        )

    if status:
        tasks = tasks.filter(Task.status == status)

    if priority:
        try:
            tasks = tasks.filter(Task.priority == int(priority))
        except ValueError:
            pass

    if user_id:
        try:
            tasks = tasks.filter(Task.user_id == int(user_id))
        except ValueError:
            pass

    results = tasks.all()
    return [t.to_dict() for t in results]

def get_stats():
    total = Task.query.count()
    pending = Task.query.filter_by(status='pending').count()
    in_progress = Task.query.filter_by(status='in_progress').count()
    done = Task.query.filter_by(status='done').count()
    cancelled = Task.query.filter_by(status='cancelled').count()

    all_tasks = Task.query.all()
    overdue_count = 0
    for t in all_tasks:
        if t.is_overdue():
            overdue_count += 1

    return {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'done': done,
        'cancelled': cancelled,
        'overdue': overdue_count,
        'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
    }
