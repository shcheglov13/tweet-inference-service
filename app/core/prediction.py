"""
Модуль для выполнения предсказаний с использованием загруженной модели FLAML.
"""
import uuid
from typing import Dict, Any

import pandas as pd

from app.config.config import config
from app.core.model_loader import model_loader
from app.features.feature_extraction import feature_extractor

logger = config.logger


class PredictionService:
    """
    Сервис для выполнения предсказаний с использованием загруженной модели.

    Отвечает за применение обученной модели к извлеченным признакам
    и формирование результата предсказания.
    """

    def __init__(self):
        """
        Инициализирует сервис предсказаний.
        """
        self.model = model_loader.load_model()
        self.threshold = model_loader.get_model_info()['threshold']

        logger.info("Инициализирован сервис предсказаний")
        logger.info(f"Используемое пороговое значение для классификации: {self.threshold}")

    def predict(self, tweet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполняет предсказание для одного твита.

        Args:
            tweet_data (Dict[str, Any]): Данные твита.

        Returns:
            Dict[str, Any]: Результат предсказания в формате
                {"request_id": "id", "tweet_id": "tweet_id", "probability": 0.87}
        """
        request_id = str(uuid.uuid4())
        tweet_id = tweet_data.get('id', 'unknown')

        logger.info(f"Выполнение предсказания для твита с ID: {tweet_id}. Request ID: {request_id}")

        try:
            # Извлекаем признаки
            features = feature_extractor.extract_features(tweet_data)

            # Преобразуем в DataFrame для модели
            features_df = pd.DataFrame([features])

            # Выполняем предсказание
            probability = self.predict_probability(features_df)

            # Формируем результат
            result = {
                "request_id": request_id,
                "tweet_id": tweet_id,
                "probability": float(probability)
            }

            # Логирование решения
            classification = "положительный" if probability >= self.threshold else "отрицательный"
            logger.info(
                f"Предсказание успешно выполнено. Tweet ID: {tweet_id}, "
                f"вероятность: {probability:.4f}, класс: {classification}"
            )

            return result

        except Exception as e:
            logger.error(f"Ошибка при выполнении предсказания для твита с ID {tweet_id}: {str(e)}")
            # В случае ошибки возвращаем результат с нулевой вероятностью
            return {
                "request_id": request_id,
                "tweet_id": tweet_id,
                "probability": 0.0
            }

    def predict_probability(self, features_df: pd.DataFrame) -> float:
        """
        Выполняет предсказание вероятности для данных признаков.

        Args:
            features_df (pd.DataFrame): DataFrame с признаками.

        Returns:
            float: Вероятность принадлежности к положительному классу.
        """
        try:
            # Получаем вероятности классов
            probabilities = self.model.predict_proba(features_df)

            # Проверяем формат выходных данных модели
            if probabilities.shape[1] != 2:
                logger.warning(
                    f"Неожиданный формат выходных данных модели: {probabilities.shape}. "
                    f"Ожидается (n_samples, 2) для бинарной классификации."
                )
                # Возвращаем вероятность по умолчанию
                return 0.5

            # Возвращаем вероятность положительного класса (класс 1)
            return float(probabilities[0, 1])

        except Exception as e:
            logger.error(f"Ошибка при вычислении вероятности: {str(e)}")
            # В случае ошибки возвращаем вероятность по умолчанию
            return 0.0


# Создаем глобальный экземпляр сервиса предсказаний
prediction_service = PredictionService()