"""
Главный файл для запуска сервиса tweet-inference-service.
"""
import uvicorn
from app.config.config import config

logger = config.logger


def main():
    """
    Главная функция для запуска сервиса.
    """
    logger.info("Запуск tweet-inference-service")

    # Получаем настройки сервиса из конфигурации
    host = config.get('service', 'host')
    port = config.get('service', 'port')
    debug = config.get('service', 'debug')

    # Запускаем сервис
    uvicorn.run(
        "app.api:app",
        host=host,
        port=port,
        reload=debug,
        log_level=config.get('logging', 'level').lower()
    )


if __name__ == "__main__":
    main()