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

def get_todos_produtos(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos WHERE ativo = 1")
    rows = cursor.fetchall()
    return [_row_to_dict(r) for r in rows]

def get_produto_por_id(db, produto_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    row = cursor.fetchone()
    return _row_to_dict(row)

def criar_produto(db, nome, descricao, preco, estoque, categoria):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
        (nome, descricao, preco, estoque, categoria)
    )
    db.commit()
    return cursor.lastrowid

def atualizar_produto(db, produto_id, nome, descricao, preco, estoque, categoria):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ? WHERE id = ?",
        (nome, descricao, preco, estoque, categoria, produto_id)
    )
    db.commit()
    return True

def deletar_produto(db, produto_id):
    # Usando Soft Delete como recomendado na PT-09
    cursor = db.cursor()
    cursor.execute("UPDATE produtos SET ativo = 0 WHERE id = ?", (produto_id,))
    db.commit()
    return True

def buscar_produtos(db, termo, categoria=None, preco_min=None, preco_max=None):
    cursor = db.cursor()
    query = "SELECT * FROM produtos WHERE ativo = 1"
    params = []
    
    if termo:
        query += " AND (nome LIKE ? OR descricao LIKE ?)"
        params.extend([f"%{termo}%", f"%{termo}%"])
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
    return [_row_to_dict(r) for r in rows]

def checar_dependencia_vendas(db, produto_id):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM itens_pedido WHERE produto_id = ?", (produto_id,))
    return cursor.fetchone()[0]
