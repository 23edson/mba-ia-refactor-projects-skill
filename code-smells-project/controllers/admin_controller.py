import logging
from database import init_db

def reset_database(db):
    cursor = db.cursor()
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM produtos")
    cursor.execute("DELETE FROM usuarios")
    db.commit()
    
    # Recria o seed do banco de dados (re-insere tabelas e registros padrões)
    init_db(db)
    logging.warning("!!! BANCO DE DADOS RESETADO PELO ADMINISTRADOR !!!")

def executar_query(db, query):
    cursor = db.cursor()
    cursor.execute(query)
    if query.strip().upper().startswith("SELECT"):
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        return result, True
    else:
        db.commit()
        return None, False
