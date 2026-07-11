import bcrypt
from models import usuario as usuario_model

def listar_usuarios(db):
    return usuario_model.get_todos_usuarios(db)

def buscar_usuario(db, usuario_id):
    usuario = usuario_model.get_usuario_por_id(db, usuario_id)
    if not usuario:
        raise ValueError("Usuário não encontrado")
    return usuario

def criar_usuario(db, dados):
    if not dados:
        raise ValueError("Dados inválidos")
        
    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()
    senha = dados.get("senha", "")
    tipo = dados.get("tipo", "cliente")

    if not nome or not email or not senha:
        raise ValueError("Nome, email e senha são obrigatórios")

    # Verifica se já existe o email cadastrado
    usuario_existente = usuario_model.get_usuario_por_email(db, email)
    if usuario_existente:
        raise ValueError("Email já cadastrado")

    # Hash da senha usando bcrypt (PT-03)
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    usuario_id = usuario_model.criar_usuario(db, nome, email, senha_hash, tipo)
    return {"id": usuario_id}

def login(db, dados):
    if not dados:
        raise ValueError("Dados inválidos")
        
    email = dados.get("email", "").strip()
    senha = dados.get("senha", "")

    if not email or not senha:
        raise ValueError("Email e senha são obrigatórios")

    usuario = usuario_model.login_usuario(db, email, senha)
    if not usuario:
        raise ValueError("Email ou senha inválidos")
        
    return usuario
