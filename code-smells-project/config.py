import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

DATABASE_PATH = os.environ.get("DATABASE_PATH", "loja.db")
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("A variável de ambiente SECRET_KEY não está configurada.")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

# Tiers de desconto e taxas para relatórios de vendas
DISCOUNT_TIER_HIGH = 10000.0
DISCOUNT_TIER_MID = 5000.0
DISCOUNT_TIER_LOW = 1000.0
DISCOUNT_RATE_HIGH = 0.1
DISCOUNT_RATE_MID = 0.05
DISCOUNT_RATE_LOW = 0.02
