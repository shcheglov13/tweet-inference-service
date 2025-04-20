"""
Инициализация API для tweet-inference-service.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config.config import config

logger = config.logger

# Создаем экземпляр FastAPI
app = FastAPI(
    title="Tweet Inference Service",
    description="Сервис для предсказания потенциала твитов с использованием модели FLAML",
    version=config.get('service', 'version'),
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавляем роутер
app.include_router(router, prefix="/api")


# Регистрируем событие запуска приложения
@app.on_event("startup")
async def startup_event():
    """
    Выполняется при запуске приложения.
    """
    logger.info("Запуск API сервиса")

    # Проверяем доступность модели
    try:
        from app.core.model_loader import model_loader
        model_loader.load_model()
        logger.info("Модель успешно загружена")
    except Exception as e:
        logger.error(f"Ошибка при загрузке модели: {str(e)}")


# Регистрируем событие завершения работы приложения
@app.on_event("shutdown")
async def shutdown_event():
    """
    Выполняется при завершении работы приложения.
    """
    logger.info("Завершение работы API сервиса")