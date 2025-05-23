"""
Модуль с Pydantic-схемами для валидации входных и выходных данных API.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class TweetInput(BaseModel):
    """
    Схема входных данных для твита.
    """
    id: str = Field(..., description="Идентификатор твита")
    created_at: str = Field(..., description="Дата и время создания твита")
    text: Optional[str] = Field(None, description="Текст твита")
    tweet_type: str = Field(..., description="Тип твита (REPLY, QUOTE, RETWEET, SINGLE)")
    image_url: Optional[str] = Field(None, description="URL изображения")
    quoted_text: Optional[str] = Field(None, description="Цитируемый текст")

    @field_validator('tweet_type')
    def validate_tweet_type(cls, v):
        """
        Валидирует тип твита.

        Args:
            v: Значение типа твита.

        Returns:
            str: Валидированное значение.

        Raises:
            ValueError: Если тип твита имеет недопустимое значение.
        """
        valid_types = ['REPLY', 'QUOTE', 'RETWEET', 'SINGLE']
        v_upper = v.upper()
        if v_upper not in valid_types:
            raise ValueError(f"Тип твита должен быть одним из {valid_types}")
        return v_upper

    @model_validator(mode='after')
    def validate_content(self):
        """
        Проверяет, что твит содержит хотя бы одно поле с значением:
        основной текст, цитируемый текст или изображение.

        Returns:
            self: Экземпляр модели.

        Raises:
            ValueError: Если твит не содержит ни одного поля с значением.
        """
        if not (self.text or self.quoted_text or self.image_url):
            raise ValueError(
                "Твит должен содержать хотя бы одно поле с значением: "
                "основной текст, цитируемый текст или изображение"
            )

        return self

    class Config:
        """
        Конфигурация схемы.
        """
        schema_extra = {
            "example": {
                "id": "1889728050276823115",
                "created_at": "2025-02-12 17:27:31.000000 +00:00",
                "text": "Пример текста твита",
                "tweet_type": "QUOTE",
                "image_url": "https://example.com/image.jpg",
                "quoted_text": "Пример цитируемого текста"
            }
        }


class PredictionResponse(BaseModel):
    """
    Схема ответа с результатом предсказания.
    """
    request_id: str = Field(..., description="Идентификатор запроса")
    tweet_id: str = Field(..., description="Идентификатор твита")
    probability: float = Field(..., description="Вероятность положительного класса", ge=0.0, le=1.0)

    class Config:
        """
        Конфигурация схемы.
        """
        schema_extra = {
            "example": {
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
                "tweet_id": "1889728050276823115",
                "probability": 0.87
            }
        }


class ErrorResponse(BaseModel):
    """
    Схема ответа с ошибкой.
    """
    error: dict = Field(..., description="Информация об ошибке")

    class Config:
        """
        Конфигурация схемы.
        """
        schema_extra = {
            "example": {
                "error": {
                    "message": "Невалидные данные твита",
                    "status_code": 400
                }
            }
        }


class HealthResponse(BaseModel):
    """
    Схема ответа для проверки работоспособности сервиса.
    """
    status: str = Field(..., description="Статус сервиса")
    version: str = Field(..., description="Версия сервиса")

    class Config:
        """
        Конфигурация схемы.
        """
        schema_extra = {
            "example": {
                "status": "ok",
                "version": "0.1.0"
            }
        }