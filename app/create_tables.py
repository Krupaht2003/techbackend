import asyncio
from .database import engine, Base
from .models.user import User  # Correct import based on directory structure

async def create_tables():
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
