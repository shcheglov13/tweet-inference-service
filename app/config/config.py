"""
Модуль для загрузки и управления конфигурацией tweet-inference-service.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any

from app.config.logging_config import setup_logging


class Config:
    """
    Класс для загрузки и хранения конфигурации сервиса.
    """

    def __init__(self, config_path: str = None):
        """
        Инициализирует конфигурацию сервиса.

        Args:
            config_path (str, optional): Путь к файлу конфигурации.
                По умолчанию ищет config.yaml в директории config.
        """
        if config_path is None:
            # Определяем путь к файлу конфигурации по умолчанию
            root_dir = Path(__file__).parent.parent.parent
            config_path = os.path.join(root_dir, 'config', 'config.yaml')

        # Проверяем существование файла
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")

        # Загружаем конфигурацию из файла
        with open(config_path, 'r', encoding='utf-8') as file:
            self._config = yaml.safe_load(file)

        # Настраиваем логирование
        self.logger = setup_logging(self._config['logging'])
        self.logger.info(f"Загружена конфигурация из {config_path}")

    def get(self, section: str, key: str = None) -> Any:
        """
        Получает значение из конфигурации.

        Args:
            section (str): Секция конфигурации.
            key (str, optional): Ключ в секции. Если не указан,
                возвращается вся секция.

        Returns:
            Any: Значение из конфигурации.

        Raises:
            KeyError: Если секция или ключ не найдены.
        """
        if section not in self._config:
            self.logger.error(f"Секция '{section}' не найдена в конфигурации")
            raise KeyError(f"Секция '{section}' не найдена в конфигурации")

        if key is None:
            return self._config[section]

        if key not in self._config[section]:
            self.logger.error(f"Ключ '{key}' не найден в секции '{section}'")
            raise KeyError(f"Ключ '{key}' не найден в секции '{section}'")

        return self._config[section][key]

    def get_all(self) -> Dict[str, Any]:
        """
        Возвращает всю конфигурацию.

        Returns:
            Dict[str, Any]: Словарь с конфигурацией.
        """
        return self._config


# Создаем глобальный экземпляр конфигурации
config = Config()