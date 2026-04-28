from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.api.routers import auth, analyze

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Uygulama başlarken çalışacak kod
    await connect_to_mongo()
    yield
    # Uygulama kapanırken çalışacak kod
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    openapi_extra={
        "components": {
            "securitySchemes": {
                "Bearer": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    }
)

# Masaüstü ve Web arayüzleri için CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Prod ortamında spesifik originler verilmeli
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(analyze.router, prefix=f"{settings.API_V1_STR}/analyze", tags=["analyze"])

@app.get("/")
async def root():
    return {
        "name": settings.PROJECT_NAME,
        "message": "AI Code Analyzer API çalışıyor",
        "docs_url": "/docs"
    }
