from database import get_db

def _row_to_dict(row):
    if not row:
        return None
    return {
        "id": row["id"],
        "nome": row["nome"],
        "descricao": row["descricao"],
        "preco": row["preco"],
        "estoque": row["estoque"],
        "categoria": row["categoria"],
        "ativo": row["ativo"],
        "criado_em": row["criado_em"]
    }

def get_todos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos WHERE ativo = 1")
    rows = cursor.fetchall()
    return [_row_to_dict(row) for row in rows]

def get_por_id(produto_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ? AND ativo = 1", (produto_id,))
    row = cursor.fetchone()
    return _row_to_dict(row)

def criar(nome, descricao, preco, estoque, categoria):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
        (nome, descricao, preco, estoque, categoria)
    )
    db.commit()
    return cursor.lastrowid

def atualizar(produto_id, nome, descricao, preco, estoque, categoria):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ? WHERE id = ? AND ativo = 1",
        (nome, descricao, preco, estoque, categoria, produto_id)
    )
    db.commit()
    return True

def deletar(produto_id):
    db = get_db()
    cursor = db.cursor()
    # Usando soft delete conforme especificado em PT-09
    cursor.execute("UPDATE produtos SET ativo = 0 WHERE id = ?", (produto_id,))
    db.commit()
    return True

def buscar(termo, categoria=None, preco_min=None, preco_max=None):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM produtos WHERE ativo = 1"
    params = []
    
    if termo:
        query += " AND (nome LIKE ? OR descricao LIKE ?)"
        term_param = f"%{termo}%"
        params.extend([term_param, term_param])
    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)
    if preco_min is not None:
        query += " AND preco >= ?"
        params.append(preco_min)
    if preco_max is not None:
        query += " AND preco <= ?"
        params.append(preco_max)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    return [_row_to_dict(row) for row in rows]
