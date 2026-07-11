from database import get_db

def _group_orders(rows):
    orders_dict = {}
    for row in rows:
        order_id = row["order_id"]
        if order_id not in orders_dict:
            orders_dict[order_id] = {
                "id": order_id,
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "criado_em": row["criado_em"],
                "itens": []
            }
        
        if row["produto_id"] is not None:
            orders_dict[order_id]["itens"].append({
                "produto_id": row["produto_id"],
                "produto_nome": row["produto_nome"] if row["produto_nome"] else "Desconhecido",
                "quantidade": row["quantidade"],
                "preco_unitario": row["preco_unitario"]
            })
    return list(orders_dict.values())

def get_pedidos_usuario(usuario_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.id as order_id, p.usuario_id, p.status, p.total, p.criado_em,
               ip.produto_id, ip.quantidade, ip.preco_unitario,
               pr.nome as produto_nome
        FROM pedidos p
        LEFT JOIN itens_pedido ip ON ip.pedido_id = p.id
        LEFT JOIN produtos pr ON pr.id = ip.produto_id
        WHERE p.usuario_id = ?
    """, (usuario_id,))
    rows = cursor.fetchall()
    return _group_orders(rows)

def get_todos_pedidos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.id as order_id, p.usuario_id, p.status, p.total, p.criado_em,
               ip.produto_id, ip.quantidade, ip.preco_unitario,
               pr.nome as produto_nome
        FROM pedidos p
        LEFT JOIN itens_pedido ip ON ip.pedido_id = p.id
        LEFT JOIN produtos pr ON pr.id = ip.produto_id
    """)
    rows = cursor.fetchall()
    return _group_orders(rows)

def criar(usuario_id, total, itens):
    db = get_db()
    cursor = db.cursor()
    
    # Inicia a transação conforme PT-06
    try:
        cursor.execute("BEGIN")
        
        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
            (usuario_id, total)
        )
        pedido_id = cursor.lastrowid
        
        for item in itens:
            # item deve conter: produto_id, quantidade, preco_unitario
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item["produto_id"], item["quantidade"], item["preco_unitario"])
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item["quantidade"], item["produto_id"])
            )
            
        db.commit()
        return pedido_id
    except Exception as e:
        db.rollback()
        raise e

def atualizar_status(pedido_id, novo_status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?",
        (novo_status, pedido_id)
    )
    db.commit()
    return True

def get_estatisticas_vendas():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(total) FROM pedidos")
    faturamento = cursor.fetchone()[0] or 0.0
    
    cursor.execute("SELECT status, COUNT(*) FROM pedidos GROUP BY status")
    status_rows = cursor.fetchall()
    status_counts = {row["status"]: row[1] for row in status_rows}
    
    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": faturamento,
        "status_counts": status_counts
    }
