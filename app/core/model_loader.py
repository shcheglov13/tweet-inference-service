"""
Модуль для загрузки и управления моделями классификации твитов.
"""
import os
import joblib
from typing import Any, Dict

from app.config.config import config

logger = config.logger


class ModelLoader:
    """
    Класс для загрузки и управления моделями машинного обучения.

    Отвечает за загрузку предобученной модели FLAML из файловой системы
    и предоставление информации о модели.
    """

    def __init__(self, model_path: str = None):
        """
        Инициализирует загрузчик моделей.

        Args:
            model_path (str, optional): Путь к файлу модели.
                По умолчанию берётся из конфигурации.
        """
        self.model_path = model_path or config.get('model', 'path')
        self.model = None
        self.model_info = {
            'version': config.get('model', 'version'),
            'threshold': config.get('model', 'threshold')
        }

        logger.info(f"Инициализирован загрузчик моделей. Путь к модели: {self.model_path}")

    def load_model(self) -> Any:
        """
        Загружает модель из файла joblib.

        Returns:
            Any: Загруженная модель FLAML.

        Raises:
            FileNotFoundError: Если файл модели не найден.
            Exception: Если возникла ошибка при загрузке модели.
        """
        if self.model is not None:
            return self.model

        try:
            if not os.path.exists(self.model_path):
                logger.error(f"Файл модели не найден: {self.model_path}")
                raise FileNotFoundError(f"Файл модели не найден: {self.model_path}")

            logger.info(f"Загрузка модели из {self.model_path}")
            self.model = joblib.load(self.model_path)

            logger.info(f"Модель успешно загружена. Версия: {self.model_info['version']}")
            return self.model

        except Exception as e:
            logger.error(f"Ошибка при загрузке модели: {str(e)}")
            raise

    def get_model_info(self) -> Dict[str, Any]:
        """
        Возвращает информацию о модели.

        Returns:
            Dict[str, Any]: Информация о модели, включая версию и пороговое значение.
        """
        return self.model_info


# Создаем глобальный экземпляр загрузчика моделей
model_loader = ModelLoader()