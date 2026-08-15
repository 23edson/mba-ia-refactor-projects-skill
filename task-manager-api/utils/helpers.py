from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except (ValueError, TypeError):
        try:
            return datetime.strptime(date_string, '%d/%m/%Y')
        except (ValueError, TypeError):
            return None

VALID_STATUSES = ['pending', 'in_progress', 'done', 'cancelled']
VALID_ROLES = ['user', 'admin', 'manager']
MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 3
MIN_PASSWORD_LENGTH = 8
DEFAULT_PRIORITY = 3
DEFAULT_COLOR = '#000000'

