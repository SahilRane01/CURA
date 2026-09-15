from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None

db_instance = MongoDB()

async def connect_to_mongo():
    # 1. Initialize the async Motor client using the URL from our settings
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db_instance.db = db_instance.client[settings.DATABASE_NAME]

    # 2. Prevent duplicate user registrations with a unique index on email
    await db_instance.db.users.create_index("email", unique=True)

    # 3. Double-booking guard index:
    # Ensures a doctor cannot have two appointments for the same start time if status is pending or confirmed
    await db_instance.db.appointments.create_index(
        [("doctor_id", 1), ("slot_start", 1)],
        unique=True,
        partialFilterExpression={"status": {"$in": ["pending", "confirmed"]}},
    )

async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()

def get_database() -> AsyncIOMotorDatabase:
    # Dependency helper to inject the DB into route handlers via Depends(get_database)
    return db_instance.db