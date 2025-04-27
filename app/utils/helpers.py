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
    Проверяет валидность данных твита.

    Args:
        tweet_data (Dict[str, Any]): Данные твита.

    Returns:
        bool: True, если данные валидны, иначе False.
    """
    # Проверяем наличие обязательных полей
    required_fields = ['id', 'created_at', 'tweet_type']
    for field in required_fields:
        if field not in tweet_data or not tweet_data[field]:
            logger.warning(f"В данных твита отсутствует обязательное поле '{field}'")
            return False

    # Проверяем тип твита
    valid_types = ['REPLY', 'QUOTE', 'RETWEET', 'SINGLE']
    tweet_type = tweet_data.get('tweet_type', '').upper()
    if tweet_type not in valid_types:
        logger.warning(f"Недопустимый тип твита: {tweet_data.get('tweet_type')}")
        return False

    # Проверяем наличие хотя бы одного поля с контентом
    text = tweet_data.get('text')
    quoted_text = tweet_data.get('quoted_text')
    image_url = tweet_data.get('image_url')

    if not (text or quoted_text or image_url):
        logger.warning(
            "Твит должен содержать хотя бы одно поле с значением: "
            "основной текст, цитируемый текст или изображение"
        )
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