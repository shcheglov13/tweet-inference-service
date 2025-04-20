"""
Модуль для предобработки данных твитов перед извлечением признаков и предсказанием.
"""
from typing import Dict, Any

from app.config.config import config

logger = config.logger


class TweetPreprocessor:
    """
    Класс для предобработки твитов перед извлечением признаков.

    Отвечает за валидацию и нормализацию данных твитов,
    подготовку данных к извлечению признаков.
    """

    def __init__(self):
        """
        Инициализирует предобработчик твитов.
        """
        logger.info("Инициализирован предобработчик твитов")

    def preprocess(self, tweet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Предобрабатывает данные твита перед извлечением признаков.

        Args:
            tweet_data (Dict[str, Any]): Данные твита.

        Returns:
            Dict[str, Any]: Предобработанные данные твита.
        """
        logger.debug(f"Предобработка твита с ID: {tweet_data.get('id', 'неизвестно')}")

        # Создаем копию данных, чтобы не изменять оригинальные
        processed_data = dict(tweet_data)

        # Проверяем наличие необходимых полей
        required_fields = ['id', 'text', 'tweet_type']
        for field in required_fields:
            if field not in processed_data:
                logger.warning(f"В данных твита отсутствует поле '{field}'")
                processed_data[field] = None

        # Проверяем и устанавливаем значения по умолчанию для опциональных полей
        if 'image_url' not in processed_data:
            processed_data['image_url'] = None

        if 'quoted_text' not in processed_data:
            processed_data['quoted_text'] = None

        if 'created_at' not in processed_data:
            processed_data['created_at'] = None

        # Проверяем тип твита и нормализуем его
        if processed_data['tweet_type'] is not None and isinstance(processed_data['tweet_type'], str):
            processed_data['tweet_type'] = processed_data['tweet_type'].upper()

            # Проверяем, что тип твита имеет допустимое значение
            valid_types = ['REPLY', 'QUOTE', 'RETWEET', 'SINGLE']
            if processed_data['tweet_type'] not in valid_types:
                logger.warning(
                    f"Неизвестный тип твита: {processed_data['tweet_type']}. "
                    f"Будет установлено значение 'SINGLE'"
                )
                processed_data['tweet_type'] = 'SINGLE'

        logger.debug(f"Предобработка твита с ID: {processed_data.get('id', 'неизвестно')} завершена")
        return processed_data