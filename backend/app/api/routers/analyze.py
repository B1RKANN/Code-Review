from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
from typing import List
from bson import ObjectId
from app.api.deps import get_current_user
from app.models.user import UserInDB
from app.models.report import ReportInDB
from app.db.mongodb import get_db
from app.analyzers.engine import AnalysisEngine
from app.services.llm import LLMService

router = APIRouter()

# Servis ve Motor örneğini al
ast_engine = AnalysisEngine()
llm_service = LLMService()

async def process_analysis(source_code: str, file_name: str, user_id: ObjectId, db):
    """
    Arka planda çalışacak olan AST analizi ve LLM isteklerini yürüten fonksiyon.
    """
    try:
        # 1. AST Analizini Çalıştır
        report = ast_engine.analyze_code(source_code, file_name)
        
        # 2. LLM İyileştirme Önerilerini İste
        suggestions = await llm_service.generate_suggestions(source_code, report)
        
        # 3. Sonucu Veritabanına Kaydet
        db_report = ReportInDB(
            user_id=user_id,
            file_name=file_name,
            report_data=report,
            llm_suggestions=suggestions
        )
        
        await db["reports"].insert_one(db_report.model_dump(by_alias=True, exclude={"id"}))
        print(f"Rapor {file_name} için başarıyla veritabanına kaydedildi.")
        
    except Exception as e:
        print(f"Arka plan analiz işlemi başarısız oldu: {str(e)}")

@router.post("/upload")
async def upload_and_analyze(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Kullanıcıdan gelen Python kodunu kabul edip, analizi arka planda başlatır.
    Masaüstü uygulamasına beklemeden bir 'işleme alındı' mesajı döner.
    """
    if not file.filename.endswith('.py'):
        raise HTTPException(status_code=400, detail="Sadece .py uzantılı Python dosyaları desteklenmektedir.")
    
    # Dosya içeriğini oku
    content = await file.read()
    try:
        source_code = content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Dosya utf-8 formatında değil.")

    # Background görevini kuyruğa ekle
    background_tasks.add_task(
        process_analysis,
        source_code,
        file.filename,
        current_user.id,
        db
    )
    
    return {"message": f"{file.filename} analizi başlatıldı. Sonuçlar birazdan hazır olacak."}

@router.get("/reports", response_model=List[dict])
async def get_my_reports(
    current_user: UserInDB = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Kullanıcının geçmiş analiz raporlarını listeler.
    """
    cursor = db["reports"].find({"user_id": current_user.id}).sort("created_at", -1)
    reports = await cursor.to_list(length=50)
    
    # _id formatını frontend'in okuyabileceği string'e dönüştür
    for r in reports:
        r["id"] = str(r.pop("_id"))
        r["user_id"] = str(r["user_id"])
        
    return reports
