import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Centralized config
DATABASE_PATH = os.environ.get("DATABASE_PATH") or os.path.join(BASE_DIR, "loja.db")
SECRET_KEY = os.environ.get("SECRET_KEY")

# For security, we ensure SECRET_KEY is set or read from env / .env file.
if not SECRET_KEY:
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    parts = line.strip().split("=", 1)
                    if len(parts) == 2 and parts[0].strip() == "SECRET_KEY":
                        SECRET_KEY = parts[1].strip().strip('"').strip("'")
    if not SECRET_KEY:
        # Fallback to avoid complete crash if not configured in tests,
        # but warn that it is insecure.
        SECRET_KEY = "fallback-desenvolvimento-insegura-123"

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

# Business logic thresholds
DISCOUNT_TIER_HIGH = 10000.0
DISCOUNT_TIER_MID = 5000.0
DISCOUNT_TIER_LOW = 1000.0

DISCOUNT_RATE_HIGH = 0.10
DISCOUNT_RATE_MID = 0.05
DISCOUNT_RATE_LOW = 0.02

CATEGORIAS_VALIDAS = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
STATUS_VALIDOS = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]
