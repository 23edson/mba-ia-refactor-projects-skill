import logging

# Configuração básica de log para a aplicação
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def notificar_criacao_pedido(pedido_id, usuario_id):
    logging.info(f"Pedido {pedido_id} criado para o usuário {usuario_id}")
    logging.info("NOTIFICAÇÃO SMS: Seu pedido foi recebido!")
    logging.info("NOTIFICAÇÃO PUSH: Novo pedido recebido pelo sistema")

def notificar_status_pedido(pedido_id, status):
    if status == "aprovado":
        logging.info(f"NOTIFICAÇÃO: Pedido {pedido_id} foi aprovado! Preparar envio.")
    elif status == "cancelado":
        logging.info(f"NOTIFICAÇÃO: Pedido {pedido_id} cancelado. Devolver estoque.")
    else:
        logging.info(f"NOTIFICAÇÃO: Status do pedido {pedido_id} atualizado para: {status}.")
