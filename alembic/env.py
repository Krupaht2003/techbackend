from logging.config import fileConfig
import asyncio
from sqlalchemy import pool
from sqlalchemy.engine import engine_from_config
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context

# Import your database models (Modify this based on your project structure)
from app.models import Base  # Ensure this path is correct

# Alembic Config object, which provides access to alembic.ini settings
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogeneration
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode for async databases."""
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    
    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_sync() -> None:
    """Run migrations in 'online' mode for sync databases."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    db_url = config.get_main_option("sqlalchemy.url")
    if "+asyncpg" in db_url:  # Check if the database URL is async
        asyncio.run(run_migrations_online())
    else:
        run_migrations_sync()
