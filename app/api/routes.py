"""
Модуль с определением маршрутов API для tweet-inference-service.
"""
from fastapi import APIRouter, HTTPException, Body, Request
from typing import Dict, Any

from app.api.schemas import TweetInput, PredictionResponse, ErrorResponse, HealthResponse
from app.core.prediction import prediction_service
from app.config.config import config
from app.utils.helpers import validate_tweet_data, format_error_response, log_api_request, log_api_response

logger = config.logger

# Создаем роутер API
router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Служебные"])
async def health_check():
    """
    Проверка работоспособности сервиса.

    Returns:
        HealthResponse: Статус и версия сервиса.
    """
    logger.info("Запрос проверки работоспособности сервиса")
    response = {
        "status": "ok",
        "version": config.get('service', 'version')
    }
    return response


@router.post("/predict", response_model=PredictionResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
             tags=["Prediction"])
async def predict(request: Request, tweet: TweetInput = Body(...)):
    """
    Выполняет предсказание для одного твита.

    Args:
        request (Request): Объект запроса FastAPI.
        tweet (TweetInput): Данные твита.

    Returns:
        PredictionResponse: Результат предсказания.

    Raises:
        HTTPException: Если данные твита невалидны или произошла ошибка при предсказании.
    """
    log_api_request("predict", tweet.dict())

    logger.info(f"Получен запрос на предсказание для твита с ID: {tweet.id}")

    # Проверяем валидность данных
    tweet_data = tweet.dict()
    if not validate_tweet_data(tweet_data):
        error_msg = "Невалидные данные твита"
        logger.warning(f"{error_msg}. ID: {tweet.id}")
        response = format_error_response(error_msg, 400)
        log_api_response("predict", response)
        raise HTTPException(status_code=400, detail=response)

    try:
        # Выполняем предсказание
        result = prediction_service.predict(tweet_data)
        logger.info(f"Предсказание успешно выполнено. Tweet ID: {tweet.id}, вероятность: {result['probability']:.4f}")
        log_api_response("predict", result)
        return result

    except Exception as e:
        error_msg = f"Ошибка при выполнении предсказания: {str(e)}"
        logger.error(f"{error_msg}. Tweet ID: {tweet.id}")
        response = format_error_response(error_msg, 500)
        log_api_response("predict", response)
        raise HTTPException(status_code=500, detail=response)


@router.get("/model/info", tags=["Модель"])
async def get_model_info():
    """
    Возвращает информацию о модели.

    Returns:
        Dict[str, Any]: Информация о модели.
    """
    logger.info("Запрос информации о модели")

    from app.core.model_loader import model_loader
    model_info = model_loader.get_model_info()

    return {
        "version": model_info["version"],
        "threshold": model_info["threshold"]
    }