import config
from models import pedido as pedido_model

def gerar_relatorio_vendas(db):
    dados = pedido_model.get_relatorio_dados(db)
    faturamento = dados["faturamento_bruto"]
    total_pedidos = dados["total_pedidos"]
    
    # Aplica regras de negócio de desconto usando as constantes da config
    desconto = 0.0
    if faturamento > config.DISCOUNT_TIER_HIGH:
        desconto = faturamento * config.DISCOUNT_RATE_HIGH
    elif faturamento > config.DISCOUNT_TIER_MID:
        desconto = faturamento * config.DISCOUNT_RATE_MID
    elif faturamento > config.DISCOUNT_TIER_LOW:
        desconto = faturamento * config.DISCOUNT_RATE_LOW

    ticket_medio = 0.0
    if total_pedidos > 0:
        ticket_medio = faturamento / total_pedidos

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": dados["pedidos_pendentes"],
        "pedidos_aprovados": dados["pedidos_aprovados"],
        "pedidos_cancelados": dados["pedidos_cancelados"],
        "ticket_medio": round(ticket_medio, 2)
    }
