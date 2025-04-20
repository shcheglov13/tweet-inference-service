"""
Инициализация приложения tweet-inference-service.
"""
from app.config.config import config

# Инициализируем логгер
logger = config.logger
logger.info("Инициализация tweet-inference-service")

__version__ = config.get('service', 'version')