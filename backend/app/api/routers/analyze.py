from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Security, Query
from typing import List, Optional
from bson import ObjectId
from app.api.deps import get_current_user
from app.models.user import UserInDB
from app.models.report import ReportInDB
from app.db.mongodb import get_db
from app.analyzers.engine import AnalysisEngine
from app.services.llm import LLMService
from app.schemas.analysis import FileScore, FileMetric, ProjectScores

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

SUPPORTED_EXTENSIONS = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.jsx': 'javascript',
    '.tsx': 'typescript',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.h': 'c',
    '.hpp': 'cpp',
    '.go': 'go',
    '.rs': 'rust',
    '.rb': 'ruby',
    '.php': 'php',
    '.cs': 'csharp',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.scala': 'scala',
    '.lua': 'lua',
    '.r': 'r',
    '.sql': 'sql',
    '.sh': 'shell',
    '.bash': 'shell',
    '.zsh': 'shell',
    '.ps1': 'powershell',
    '.ex': 'elixir',
    '.exs': 'elixir',
    '.erl': 'erlang',
    '.hs': 'haskell',
    '.clj': 'clojure',
    '.cljs': 'clojure',
    '.fs': 'fsharp',
    '.fsx': 'fsharp',
    '.dart': 'dart',
    '.vue': 'vue',
    '.svelte': 'svelte',
}


@router.post("/upload")
async def upload_and_analyze(
    file: UploadFile = File(...),
    current_user: UserInDB = Security(get_current_user),
    db = Depends(get_db)
):
    """
    Kullanıcıdan gelen kodu kabul edip, analizi çalıştırıp sonucu döner.
    """
    file_ext = '.' + file.filename.rsplit('.', 1)[-1] if '.' in file.filename else ''
    if file_ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Desteklenmeyen dosya uzantısı. Desteklenen uzantılar: {', '.join(SUPPORTED_EXTENSIONS.keys())}"
        )
    
    content = await file.read()
    try:
        source_code = content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Dosya utf-8 formatında değil.")

    language = SUPPORTED_EXTENSIONS.get(file_ext, 'python')
    
    # AST analizi sadece Python dosyaları için çalışır
    # Diğer diller için boş rapor döner, LLM analizi yapılır
    if language == "python":
        report = ast_engine.analyze_code(source_code, file.filename)
    else:
        from app.schemas.analysis import AnalysisReport
        report = AnalysisReport(file_name=file.filename, issues=[], total_issues=0)
    
    suggestions = await llm_service.generate_suggestions(source_code, report, language=language)

    db_report = ReportInDB(
        user_id=current_user.id,
        file_name=file.filename,
        report_data=report,
        llm_suggestions=suggestions
    )
    
    result = await db["reports"].insert_one(db_report.model_dump(by_alias=True, exclude={"id"}))
    
    return {
        "report_id": str(result.inserted_id),
        "file_name": file.filename,
        "report": report,
        "llm_suggestions": suggestions
    }

@router.get("/reports", response_model=List[dict])
async def get_my_reports(
    current_user: UserInDB = Security(get_current_user),
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
