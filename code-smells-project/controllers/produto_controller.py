from models import produto as produto_model

CATEGORIAS_VALIDAS = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]

def listar_produtos(db):
    return produto_model.get_todos_produtos(db)

def buscar_produto(db, produto_id):
    produto = produto_model.get_produto_por_id(db, produto_id)
    if not produto:
        raise ValueError("Produto não encontrado")
    return produto

def validar_dados_produto(dados, is_update=False):
    if not dados:
        raise ValueError("Dados inválidos")
    
    if not is_update:
        if "nome" not in dados:
            raise ValueError("Nome é obrigatório")
        if "preco" not in dados:
            raise ValueError("Preço é obrigatório")
        if "estoque" not in dados:
            raise ValueError("Estoque é obrigatório")

    nome = dados.get("nome")
    preco = dados.get("preco")
    estoque = dados.get("estoque")
    categoria = dados.get("categoria", "geral")

    if nome is not None:
        if len(nome) < 2:
            raise ValueError("Nome muito curto")
        if len(nome) > 200:
            raise ValueError("Nome muito longo")

    if preco is not None:
        try:
            preco_val = float(preco)
            if preco_val < 0:
                raise ValueError("Preço não pode ser negativo")
        except ValueError:
            raise ValueError("Preço deve ser um número válido")

    if estoque is not None:
        try:
            estoque_val = int(estoque)
            if estoque_val < 0:
                raise ValueError("Estoque não pode ser negativo")
        except ValueError:
            raise ValueError("Estoque deve ser um número inteiro válido")

    if categoria not in CATEGORIAS_VALIDAS:
        raise ValueError(f"Categoria inválida. Válidas: {CATEGORIAS_VALIDAS}")

def criar_produto(db, dados):
    validar_dados_produto(dados)
    
    nome = dados["nome"]
    descricao = dados.get("descricao", "")
    preco = float(dados["preco"])
    estoque = int(dados["estoque"])
    categoria = dados.get("categoria", "geral")
    
    novo_id = produto_model.criar_produto(db, nome, descricao, preco, estoque, categoria)
    return {"id": novo_id}

def atualizar_produto(db, produto_id, dados):
    # Verifica se produto existe
    produto_existente = produto_model.get_produto_por_id(db, produto_id)
    if not produto_existente:
        raise ValueError("Produto não encontrado")
        
    validar_dados_produto(dados, is_update=True)
    
    nome = dados.get("nome", produto_existente["nome"])
    descricao = dados.get("descricao", produto_existente["descricao"])
    preco = float(dados.get("preco", produto_existente["preco"]))
    estoque = int(dados.get("estoque", produto_existente["estoque"]))
    categoria = dados.get("categoria", produto_existente["categoria"])
    
    produto_model.atualizar_produto(db, produto_id, nome, descricao, preco, estoque, categoria)
    return True

def deletar_produto(db, produto_id):
    # Verifica se produto existe
    produto = produto_model.get_produto_por_id(db, produto_id)
    if not produto:
        raise ValueError("Produto não encontrado")
        
    # PT-09: Impedir hard delete se existirem pedidos vinculados
    vendas_count = produto_model.checar_dependencia_vendas(db, produto_id)
    if vendas_count > 0:
        raise ValueError("Produto possui pedidos e não pode ser removido")
        
    produto_model.deletar_produto(db, produto_id)
    return True

def buscar_produtos(db, termo, categoria=None, preco_min=None, preco_max=None):
    if preco_min is not None:
        preco_min = float(preco_min)
    if preco_max is not None:
        preco_max = float(preco_max)
    return produto_model.buscar_produtos(db, termo, categoria, preco_min, preco_max)
