from models import usuario as usuario_model
import bcrypt

def listar_usuarios():
    return usuario_model.get_todos()

def buscar_usuario(usuario_id):
    usuario = usuario_model.get_por_id(usuario_id)
    if not usuario:
        raise KeyError("Usuário não encontrado")
    return usuario

def criar_usuario(nome, email, senha):
    if not nome or not email or not senha:
        raise ValueError("Nome, email e senha são obrigatórios")
    
    # Hashing password
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Verificar se email já existe
    usuario_existente = usuario_model.get_por_email(email)
    if usuario_existente:
        raise ValueError("Email já cadastrado")
        
    usuario_id = usuario_model.criar(nome, email, senha_hash)
    return {"id": usuario_id}

def login(email, senha):
    if not email or not senha:
        raise ValueError("Email e senha são obrigatórios")
        
    usuario = usuario_model.get_por_email(email)
    if not usuario:
        raise PermissionError("Email ou senha inválidos")
        
    # Verificar a senha usando bcrypt
    stored_hash = usuario.get("senha")
    if not stored_hash or not bcrypt.checkpw(senha.encode('utf-8'), stored_hash.encode('utf-8')):
        raise PermissionError("Email ou senha inválidos")
        
    # Remover senha do dicionário de retorno
    usuario.pop("senha", None)
    return usuario
