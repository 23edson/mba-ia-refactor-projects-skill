from database import db
from models.category import Category
from models.task import Task

def list_categories():
    categories = Category.query.all()
    result = []
    for c in categories:
        cat_data = c.to_dict()
        cat_data['task_count'] = Task.query.filter_by(category_id=c.id).count()
        result.append(cat_data)
    return result

def create_category(name, description='', color='#000000'):
    if not name:
        raise ValueError('Nome é obrigatório')

    category = Category()
    category.name = name
    category.description = description
    category.color = color

    db.session.add(category)
    db.session.commit()
    return category.to_dict()

def update_category(cat_id, data):
    cat = Category.query.get(cat_id)
    if not cat:
        raise ValueError('Categoria não encontrada')

    if 'name' in data:
        cat.name = data['name']
    if 'description' in data:
        cat.description = data['description']
    if 'color' in data:
        cat.color = data['color']

    db.session.commit()
    return cat.to_dict()

def delete_category(cat_id):
    cat = Category.query.get(cat_id)
    if not cat:
        raise ValueError('Categoria não encontrada')

    db.session.delete(cat)
    db.session.commit()
