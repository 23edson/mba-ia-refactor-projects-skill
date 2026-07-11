from models import produto as produto_model
import config

def listar_produtos():
    return produto_model.get_todos()

def buscar_produto(produto_id):
    produto = produto_model.get_por_id(produto_id)
    if not produto:
        raise KeyError("Produto não encontrado")
    return produto

def criar_produto(nome, descricao, preco, estoque, categoria):
    if not nome:
        raise ValueError("Nome é obrigatório")
    if preco is None:
        raise ValueError("Preço é obrigatório")
    if estoque is None:
        raise ValueError("Estoque é obrigatório")

    try:
        preco = float(preco)
        estoque = int(estoque)
    except (TypeError, ValueError):
        raise ValueError("Preço e estoque devem ser numéricos")

    if preco < 0:
        raise ValueError("Preço não pode ser negativo")
    if estoque < 0:
        raise ValueError("Estoque não pode ser negativo")
    if len(nome) < 2:
        raise ValueError("Nome muito curto")
    if len(nome) > 200:
        raise ValueError("Nome muito longo")

    if categoria not in config.CATEGORIAS_VALIDAS:
        raise ValueError(f"Categoria inválida. Válidas: {config.CATEGORIAS_VALIDAS}")

    produto_id = produto_model.criar(nome, descricao, preco, estoque, categoria)
    return {"id": produto_id}

def atualizar_produto(produto_id, nome, descricao, preco, estoque, categoria):
    # Verificar se o produto existe
    produto = produto_model.get_por_id(produto_id)
    if not produto:
        raise KeyError("Produto não encontrado")

    if not nome:
        raise ValueError("Nome é obrigatório")
    if preco is None:
        raise ValueError("Preço é obrigatório")
    if estoque is None:
        raise ValueError("Estoque é obrigatório")

    try:
        preco = float(preco)
        estoque = int(estoque)
    except (TypeError, ValueError):
        raise ValueError("Preço e estoque devem ser numéricos")

    if preco < 0:
        raise ValueError("Preço não pode ser negativo")
    if estoque < 0:
        raise ValueError("Estoque não pode ser negativo")
    if len(nome) < 2:
        raise ValueError("Nome muito curto")
    if len(nome) > 200:
        raise ValueError("Nome muito longo")

    if categoria not in config.CATEGORIAS_VALIDAS:
        raise ValueError(f"Categoria inválida. Válidas: {config.CATEGORIAS_VALIDAS}")

    produto_model.atualizar(produto_id, nome, descricao, preco, estoque, categoria)
    return True

def deletar_produto(produto_id):
    # Verificar se o produto existe
    produto = produto_model.get_por_id(produto_id)
    if not produto:
        raise KeyError("Produto não encontrado")

    # M-4: Impedir a exclusão caso o produto tenha pedidos associados (integridade referencial)
    # Mas wait, does it have orders associated?
    # We can check by checking if there's any order with this product in itens_pedido.
    # To keep it simple, we can query if product exists in any item of order. Let's do a quick check.
    # Let's see: we can implement a check in model or directly.
    # Let's add a database check in models/pedido.py or check it here. Let's check it in the model
    # or write a query. Actually, we can check database if we want to be safe.
    # Let's see: can we add a check in models/produto.py or models/pedido.py?
    # Let's query SQLite for checking if this product is in any itens_pedido.
    from database import get_db
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM itens_pedido WHERE produto_id = ?", (produto_id,))
    count = cursor.fetchone()[0]
    if count > 0:
        raise ValueError("Produto possui pedidos associados e não pode ser removido fisicamente.")

    produto_model.deletar(produto_id)
    return True

def buscar_produtos(termo, categoria=None, preco_min=None, preco_max=None):
    try:
        if preco_min is not None:
            preco_min = float(preco_min)
        if preco_max is not None:
            preco_max = float(preco_max)
    except (TypeError, ValueError):
        raise ValueError("Limites de preço devem ser numéricos")

    return produto_model.buscar(termo, categoria, preco_min, preco_max)
