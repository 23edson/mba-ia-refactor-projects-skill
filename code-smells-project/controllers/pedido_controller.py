from models import pedido as pedido_model
from models import produto as produto_model
from models import usuario as usuario_model
from services import notification_service

def criar_pedido(db, dados):
    if not dados:
        raise ValueError("Dados inválidos")

    usuario_id = dados.get("usuario_id")
    itens = dados.get("itens", [])

    if not usuario_id:
        raise ValueError("Usuario ID é obrigatório")
    if not itens or len(itens) == 0:
        raise ValueError("Pedido deve ter pelo menos 1 item")

    # Verifica se usuário existe
    usuario = usuario_model.get_usuario_por_id(db, usuario_id)
    if not usuario:
        raise ValueError("Usuário não encontrado")

    total = 0.0
    itens_processados = []

    for item in itens:
        produto_id = item.get("produto_id")
        quantidade = item.get("quantidade")

        if not produto_id or not quantidade:
            raise ValueError("Item do pedido inválido (deve conter produto_id e quantidade)")

        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero")
        except ValueError:
            raise ValueError("Quantidade inválida")

        # Busca produto e valida estoque
        produto = produto_model.get_produto_por_id(db, produto_id)
        if not produto:
            raise ValueError(f"Produto {produto_id} não encontrado")
        
        if produto["estoque"] < quantidade:
            raise ValueError(f"Estoque insuficiente para {produto['nome']}")

        total += produto["preco"] * quantidade
        itens_processados.append({
            "produto_id": produto_id,
            "quantidade": quantidade,
            "preco_unitario": produto["preco"]
        })

    # Cria o pedido no banco usando transação atômica (PT-06)
    resultado = pedido_model.criar_pedido(db, usuario_id, total, itens_processados)

    # Envia notificações simuladas utilizando o serviço dedicado (PT-05 / H-1)
    notification_service.send_order_notifications(resultado["pedido_id"], usuario_id)

    return resultado

def listar_todos_pedidos(db):
    return pedido_model.get_todos_pedidos(db)

def listar_pedidos_usuario(db, usuario_id):
    # Verifica se usuário existe
    usuario = usuario_model.get_usuario_por_id(db, usuario_id)
    if not usuario:
        raise ValueError("Usuário não encontrado")
    return pedido_model.get_pedidos_usuario(db, usuario_id)

def atualizar_status_pedido(db, pedido_id, dados):
    if not dados:
        raise ValueError("Dados inválidos")
        
    novo_status = dados.get("status", "")
    if novo_status not in ["pendente", "aprovado", "enviado", "entregue", "cancelado"]:
        raise ValueError("Status inválido")

    # Verifica se o pedido existe antes de atualizar
    # (Poderíamos ter uma consulta rápida no model, ou buscar todos e filtrar)
    # Por simplicidade, podemos fazer o update direto ou uma checagem rápida.
    # Vamos fazer a atualização.
    pedido_model.atualizar_status_pedido(db, pedido_id, novo_status)

    # Dispara a notificação adequada (PT-05 / H-1)
    notification_service.send_status_notifications(pedido_id, novo_status)
    return True
