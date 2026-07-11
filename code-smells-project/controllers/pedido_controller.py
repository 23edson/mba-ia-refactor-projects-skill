from models import pedido as pedido_model
from models import produto as produto_model
from models import usuario as usuario_model
from services import notification_service
import config

def criar_pedido(usuario_id, itens):
    if not usuario_id:
        raise ValueError("Usuario ID é obrigatório")
    if not itens or len(itens) == 0:
        raise ValueError("Pedido deve ter pelo menos 1 item")

    # Verificar se o usuário existe
    usuario = usuario_model.get_por_id(usuario_id)
    if not usuario:
        raise ValueError(f"Usuário {usuario_id} não encontrado")

    total = 0.0
    items_to_save = []

    for item in itens:
        produto_id = item.get("produto_id")
        quantidade = item.get("quantidade")
        if not produto_id or quantidade is None or quantidade <= 0:
            raise ValueError("Item inválido (produto_id e quantidade maior que zero são obrigatórios)")

        produto = produto_model.get_por_id(produto_id)
        if not produto:
            raise ValueError(f"Produto {produto_id} não encontrado")
        
        if produto["estoque"] < quantidade:
            raise ValueError(f"Estoque insuficiente para {produto['nome']}")
        
        total += produto["preco"] * quantidade
        items_to_save.append({
            "produto_id": produto_id,
            "quantidade": quantidade,
            "preco_unitario": produto["preco"]
        })

    # Criar o pedido com transação
    pedido_id = pedido_model.criar(usuario_id, total, items_to_save)

    # Chamar serviço de notificação
    notification_service.notificar_criacao_pedido(pedido_id, usuario_id)

    return {"pedido_id": pedido_id, "total": total}

def listar_pedidos_usuario(usuario_id):
    # Verificar se usuário existe
    usuario = usuario_model.get_por_id(usuario_id)
    if not usuario:
        raise ValueError("Usuário não encontrado")
    return pedido_model.get_pedidos_usuario(usuario_id)

def listar_todos_pedidos():
    return pedido_model.get_todos_pedidos()

def atualizar_status_pedido(pedido_id, novo_status):
    if novo_status not in config.STATUS_VALIDOS:
        raise ValueError("Status inválido")

    # Verificar se o pedido existe (podemos buscar todos e filtrar ou implementar no model)
    # Para ser simples, listamos todos os pedidos e vemos se id existe
    todos = pedido_model.get_todos_pedidos()
    pedido_existe = any(p["id"] == pedido_id for p in todos)
    if not pedido_existe:
        raise KeyError("Pedido não encontrado")

    pedido_model.atualizar_status(pedido_id, novo_status)

    # Notificar status atualizado
    notification_service.notificar_status_pedido(pedido_id, novo_status)
    return True

def relatorio_vendas():
    stats = pedido_model.get_estatisticas_vendas()
    
    total_pedidos = stats["total_pedidos"]
    faturamento_bruto = stats["faturamento_bruto"]
    status_counts = stats["status_counts"]
    
    # Lógica de negócio: cálculo de desconto com base nos limites e taxas em config.py
    desconto = 0.0
    if faturamento_bruto > config.DISCOUNT_TIER_HIGH:
        desconto = faturamento_bruto * config.DISCOUNT_RATE_HIGH
    elif faturamento_bruto > config.DISCOUNT_TIER_MID:
        desconto = faturamento_bruto * config.DISCOUNT_RATE_MID
    elif faturamento_bruto > config.DISCOUNT_TIER_LOW:
        desconto = faturamento_bruto * config.DISCOUNT_RATE_LOW

    ticket_medio = faturamento_bruto / total_pedidos if total_pedidos > 0 else 0.0

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento_bruto, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento_bruto - desconto, 2),
        "pedidos_pendentes": status_counts.get("pendente", 0),
        "pedidos_aprovados": status_counts.get("aprovado", 0),
        "pedidos_cancelados": status_counts.get("cancelado", 0),
        "ticket_medio": round(ticket_medio, 2)
    }
