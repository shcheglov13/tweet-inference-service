"""
Модуль для настройки логирования в tweet-inference-service.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(config):
    """
    Настраивает логирование для сервиса согласно конфигурации.

    Args:
        config (dict): Конфигурация логирования из config.yaml

    Returns:
        logging.Logger: Настроенный логгер
    """
    # Создаем директорию для логов, если она не существует
    log_dir = Path(os.path.dirname(config['file']))
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

    # Настраиваем корневой логгер
    logger = logging.getLogger('tweet-inference-service')
    logger.setLevel(config['level'])

    # Создаем форматтер для логов
    formatter = logging.Formatter(
        fmt=config['format'],
        datefmt=config['date_format']
    )

    # Настраиваем вывод в файл с ротацией
    file_handler = RotatingFileHandler(
        filename=config['file'],
        maxBytes=config['max_bytes'],
        backupCount=config['backup_count'],
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Настраиваем вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger