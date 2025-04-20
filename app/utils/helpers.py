"""
Модуль с вспомогательными функциями для tweet-inference-service.
"""
import uuid
from typing import Dict, Any

from app.config.config import config

logger = config.logger


def generate_request_id() -> str:
    """
    Генерирует уникальный идентификатор запроса.

    Returns:
        str: Уникальный идентификатор запроса.
    """
    return str(uuid.uuid4())


def validate_tweet_data(tweet_data: Dict[str, Any]) -> bool:
    """
    Проверяет наличие необходимых полей в данных твита.

    Args:
        tweet_data (Dict[str, Any]): Данные твита.

    Returns:
        bool: True, если данные валидны, иначе False.
    """
    # Проверяем наличие обязательных полей
    required_fields = ['id']
    for field in required_fields:
        if field not in tweet_data:
            logger.warning(f"В данных твита отсутствует обязательное поле '{field}'")
            return False

    return True


def format_error_response(message: str, status_code: int = 400) -> Dict[str, Any]:
    """
    Форматирует ответ с ошибкой.

    Args:
        message (str): Сообщение об ошибке.
        status_code (int, optional): Код статуса HTTP. По умолчанию 400.

    Returns:
        Dict[str, Any]: Отформатированный ответ с ошибкой.
    """
    return {
        "error": {
            "message": message,
            "status_code": status_code
        }
    }


def log_api_request(endpoint: str, request_data: Dict[str, Any]) -> None:
    """
    Логирует информацию о входящем API-запросе.

    Args:
        endpoint (str): Имя эндпоинта API.
        request_data (Dict[str, Any]): Данные запроса.
    """
    tweet_id = request_data.get('id', 'неизвестно')
    logger.info(f"API-запрос к эндпоинту '{endpoint}'. Tweet ID: {tweet_id}")


def log_api_response(endpoint: str, response_data: Dict[str, Any]) -> None:
    """
    Логирует информацию об ответе API.

    Args:
        endpoint (str): Имя эндпоинта API.
        response_data (Dict[str, Any]): Данные ответа.
    """
    if 'error' in response_data:
        logger.warning(
            f"API-ошибка в эндпоинте '{endpoint}': "
            f"{response_data['error'].get('message', 'неизвестная ошибка')}"
        )
    else:
        tweet_id = response_data.get('tweet_id', 'неизвестно')
        request_id = response_data.get('request_id', 'неизвестно')
        logger.info(
            f"API-ответ от эндпоинта '{endpoint}'. "
            f"Tweet ID: {tweet_id}, Request ID: {request_id}"
        )