"""
Модуль для извлечения признаков из твитов с использованием пакета tweet-features.
"""
from typing import Dict, Any, List

from tweet_features.config import default_config
from tweet_features.pipeline import FeaturePipeline

from app.config.config import config
from app.preprocessing.preprocessing import TweetPreprocessor

logger = config.logger


class FeatureExtractor:
    """
    Класс для извлечения признаков из твитов с использованием пакета tweet-features.

    Отвечает за создание и применение пайплайна извлечения признаков,
    взаимодействие с библиотекой tweet-features.
    """

    def __init__(self):
        """
        Инициализирует экстрактор признаков с настройками из конфигурации.
        """
        # Инициализируем предобработчик
        self.preprocessor = TweetPreprocessor()

        # Получаем настройки для tweet-features из конфигурации
        tweet_features_settings = config.get('tweet_features')

        # Инициализируем пайплайн извлечения признаков
        self.feature_pipeline = FeaturePipeline(
            config=default_config,
            use_structural=tweet_features_settings.get('use_structural', True),
            use_text=tweet_features_settings.get('use_text', True),
            use_image=tweet_features_settings.get('use_image', True),
            use_emotional=tweet_features_settings.get('use_emotional', True),
            use_bert_embeddings=tweet_features_settings.get('use_bert_embeddings', True)
        )

        logger.info("Инициализирован экстрактор признаков с использованием tweet-features")

        # Логируем, какие типы признаков будут извлекаться
        feature_types = []
        if tweet_features_settings.get('use_structural', True):
            feature_types.append('структурные')
        if tweet_features_settings.get('use_text', True):
            feature_types.append('текстовые')
        if tweet_features_settings.get('use_image', True):
            feature_types.append('визуальные')
        if tweet_features_settings.get('use_emotional', True):
            feature_types.append('эмоциональные')

        logger.info(f"Типы извлекаемых признаков: {', '.join(feature_types)}")

    def extract_features(self, tweet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Извлекает признаки из данных твита.

        Args:
            tweet_data (Dict[str, Any]): Данные твита.

        Returns:
            Dict[str, Any]: Извлечённые признаки.

        Raises:
            Exception: Если возникла ошибка при извлечении признаков.
        """
        logger.info(f"Извлечение признаков для твита с ID: {tweet_data.get('id', 'неизвестно')}")

        try:
            # Предобрабатываем данные
            preprocessed_data = self.preprocessor.preprocess(tweet_data)

            # Извлекаем признаки
            features = self.feature_pipeline.extract_single(preprocessed_data)

            logger.info(f"Признаки успешно извлечены для твита с ID: {preprocessed_data.get('id', 'неизвестно')}")
            logger.debug(f"Извлечено {len(features)} признаков")

            return features
        except Exception as e:
            logger.error(f"Ошибка при извлечении признаков: {str(e)}")
            raise Exception(f"Ошибка при извлечении признаков: {str(e)}")

    def get_feature_names(self) -> List[str]:
        """
        Возвращает список всех имен признаков, извлекаемых пайплайном.

        Returns:
            List[str]: Список имен признаков.
        """
        feature_names = list(self.feature_pipeline.get_feature_names())
        logger.debug(f"Доступные признаки: {', '.join(feature_names)}")
        return feature_names


# Создаем глобальный экземпляр экстрактора признаков
feature_extractor = FeatureExtractor()