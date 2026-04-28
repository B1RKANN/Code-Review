from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class DataBase:
    client: AsyncIOMotorClient = None
    db = None

db_instance = DataBase()

async def connect_to_mongo():
    try:
        db_instance.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db_instance.db = db_instance.client[settings.DATABASE_NAME]
        # Bağlantıyı test et
        await db_instance.client.admin.command('ping')
        print("MongoDB bağlantısı başarılı.")
    except Exception as e:
        print(f"MongoDB bağlantı hatası: {e}")

async def close_mongo_connection():
    if db_instance.client is not None:
        db_instance.client.close()
        print("MongoDB bağlantısı kapatıldı.")

def get_db():
    return db_instance.db
