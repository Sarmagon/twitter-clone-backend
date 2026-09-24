"""
Конфигурация Alembic для миграций базы данных.

Этот файл настраивает Alembic для работы с нашим приложением.
Использует синхронный движок SQLAlchemy для выполнения миграций,
так как миграции - это разовые операции, и асинхронность здесь не критична.
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

import app.models  # noqa: F401 -- register all tables for Alembic metadata
from alembic import context

# Импортируем настройки приложения
from app.config import settings

# Импортируем базовый класс и все модели
# Это необходимо, чтобы Alembic мог обнаружить изменения в моделях
from app.database import Base

# это объект Alembic Config, который дает доступ к файлу alembic.ini
config = context.config

# Интерпретируем файл config для настройки логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata - это метаданные наших моделей
# Alembic использует их для автогенерации миграций
target_metadata = Base.metadata

# Переопределяем URL подключения из настроек приложения
# Используем синхронный драйвер psycopg2 для миграций
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url("postgresql+psycopg2")
    .render_as_string(hide_password=False)
    .replace("%", "%%"),
)


def run_migrations_offline() -> None:
    """
    Запуск миграций в 'оффлайн' режиме.

    Генерирует SQL-скрипты без подключения к базе данных.
    Используется для создания скриптов, которые можно выполнить вручную.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Запуск миграций в 'онлайн' режиме.

    Подключается к базе данных и применяет миграции напрямую.
    Это основной режим работы Alembic.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
