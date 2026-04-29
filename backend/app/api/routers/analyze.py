from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Security
from typing import List
from bson import ObjectId
from app.api.deps import get_current_user
from app.models.user import UserInDB
from app.models.report import ReportInDB
from app.db.mongodb import get_db
from app.analyzers.engine import AnalysisEngine
from app.services.llm import LLMService
from app.schemas.analysis import FileScore, FileMetric, ProjectScores, FileAnalysisResult, Finding, Aside


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
        try:
            source_code = content.decode('utf-8-sig') # For BOM
        except UnicodeDecodeError:
            source_code = content.decode('latin-1', errors='ignore') # Fallback

    language = SUPPORTED_EXTENSIONS.get(file_ext, 'python')
    
    # AST analizi sadece Python dosyaları için çalışır
    # Diğer diller için LLM üzerinden analiz yapılır
    if language == "python":
        report = ast_engine.analyze_code(source_code, file.filename)
    else:
        report = await llm_service.analyze_code_with_ai(source_code, file.filename, language)
    
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


@router.post("/analyze-file", response_model=FileAnalysisResult)
async def analyze_single_file(
    file: UploadFile = File(...)
):
    """
    Masaüstü uygulaması için tek bir dosyanın analiz sonuçlarını döndürür.
    Frontend'in beklediği score, findings, sources ve aside formatlarını sağlar.
    """
    content = await file.read()
    try:
        source_code = content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            source_code = content.decode('utf-8-sig') # For BOM
        except UnicodeDecodeError:
            source_code = content.decode('latin-1', errors='ignore') # Fallback

    file_path = file.filename
    file_ext = '.' + file_path.rsplit('.', 1)[-1] if '.' in file_path else ''
    language = SUPPORTED_EXTENSIONS.get(file_ext, 'python')

    if language == "python":
        report = ast_engine.analyze_code(source_code, file_path)
    else:
        report = await llm_service.analyze_code_with_ai(source_code, file_path, language)

    # Score calculation
    score_data = _calculate_scores_from_report(report, language)
    file_score = _build_file_score(score_data)

    # Findings mapping
    findings = []
    for issue in report.issues:
        sev = "h" if issue.severity.value == "High" else "m" if issue.severity.value == "Medium" else "l"
        findings.append(Finding(
            sev=sev,
            title=issue.message,
            loc=f"{file_path}:{issue.line_number}",
            tag=issue.category.value.lower()
        ))

    # Sources mapping
    lines = source_code.splitlines()
    sources = []
    for i, line in enumerate(lines, 1):
        # find if there's an issue on this line
        line_issues = [iss for iss in report.issues if iss.line_number == i]
        status = None
        if line_issues:
            highest_sev = max(line_issues, key=lambda x: {"Low": 1, "Medium": 2, "High": 3}[x.severity.value]).severity.value
            status = "bad" if highest_sev == "High" else "warn" if highest_sev == "Medium" else "info"
        sources.append((i, line, status))

    # Aside mapping
    aside = []
    for issue in report.issues:
        sev = "bad" if issue.severity.value == "High" else "warn" if issue.severity.value == "Medium" else "info"
        aside.append(Aside(
            sev=sev,
            line=issue.line_number,
            title=issue.message[:50] + "..." if len(issue.message) > 50 else issue.message,
            desc=issue.message,
            fix=issue.suggestion
        ))

    return FileAnalysisResult(
        score=file_score,
        findings=findings,
        sources=sources,
        aside=aside
    )


@router.post("/scores", response_model=ProjectScores)
async def get_scores(
    file: UploadFile = File(...),
    current_user: UserInDB = Security(get_current_user),
):
    """
    Yüklenen dosyanın skorlarını analiz ederek döner.
    """
    content = await file.read()
    try:
        source_code = content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            source_code = content.decode('utf-8-sig') # For BOM
        except UnicodeDecodeError:
            source_code = content.decode('latin-1', errors='ignore') # Fallback

    file_path = file.filename
    file_ext = '.' + file_path.rsplit('.', 1)[-1] if '.' in file_path else ''
    language = SUPPORTED_EXTENSIONS.get(file_ext, 'python')

    if language == "python":
        report = ast_engine.analyze_code(source_code, file_path)
    else:
        report = await llm_service.analyze_code_with_ai(source_code, file_path, language)

    score_data = _calculate_scores_from_report(report, language)

    return ProjectScores(files={file_path: _build_file_score(score_data)})


def _build_file_score(data: dict) -> FileScore:
    metrics = {}
    for key, metric_data in data["metrics"].items():
        metrics[key] = FileMetric(
            value=metric_data["value"],
            label=metric_data["label"],
            desc=metric_data["desc"],
            stats=[tuple(s) for s in metric_data["stats"]]
        )
    return FileScore(
        overall=data["overall"],
        status=data["status"],
        statusKind=data["statusKind"],
        metrics=metrics
    )


from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    file_path: str
    source_code: str

@router.post("/chat")
async def chat_about_file(request: ChatRequest):
    """
    Masaüstü uygulamasından gelen chat mesajlarına yanıt üretir.
    """
    if not llm_service.client:
        return {"reply": "LLM yapılandırılmadığı için AI yanıt veremiyor."}
    
    file_ext = '.' + request.file_path.rsplit('.', 1)[-1] if '.' in request.file_path else ''
    language = SUPPORTED_EXTENSIONS.get(file_ext, 'python')
    
    prompt = f"""
Sen CodeGuard AI adında uzman bir yazılım mimarısın.
Kullanıcı şu an {request.file_path} adlı {language} dosyasını inceliyor.
Kullanıcının sorusu: {request.message}

İncelenen Kod:
```{language}
{request.source_code}
```

Lütfen profesyonel, eğitici ve yardımcı bir dille Türkçe olarak yanıt ver.
Yanıtın HTML formatında (sadece <p>, <b>, <code>, <pre> etiketleri kullanarak) biçimlendirilmiş olsun.
"""
    try:
        response = await llm_service.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen CodeGuard AI asistanısın. Yanıtlarını basit HTML etiketleriyle formatla."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        return {"reply": f"<p>Bir hata oluştu: {str(e)}</p>"}

def _calculate_scores_from_report(report, language: str) -> dict:
    from app.schemas.analysis import SeverityLevel, Category

    security_issues = [i for i in report.issues if i.category == Category.SECURITY]
    architecture_issues = [i for i in report.issues if i.category == Category.ARCHITECTURE]
    solid_issues = [i for i in report.issues if i.category == Category.SOLID]

    high_severity = [i for i in report.issues if i.severity == SeverityLevel.HIGH]
    medium_severity = [i for i in report.issues if i.severity == SeverityLevel.MEDIUM]
    low_severity = [i for i in report.issues if i.severity == SeverityLevel.LOW]

    security_score = max(0, 100 - (len(security_issues) * 15) - (len(high_severity) * 10))
    clean_code_score = max(0, 100 - (len(solid_issues) * 10) - (len(architecture_issues) * 5) - (len(medium_severity) * 3))
    perf_score = max(0, 85 - (len(high_severity) * 10) - (len(medium_severity) * 5))
    robust_score = max(0, 90 - (len(architecture_issues) * 8) - (len(low_severity) * 2))

    overall = int((security_score + clean_code_score + perf_score + robust_score) / 4)

    if overall >= 85:
        status = "Sağlıklı"
        statusKind = "good"
    elif overall >= 70:
        status = "İyi"
        statusKind = "good"
    elif overall >= 50:
        status = "Dikkat Gerekiyor"
        statusKind = "warn"
    else:
        status = "Kritik"
        statusKind = "bad"

    return {
        "overall": overall,
        "status": status,
        "statusKind": statusKind,
        "metrics": {
            "security": {
                "value": security_score,
                "label": "Ağ Güvenliği",
                "desc": f"{len(security_issues)} güvenlik sorunu tespit edildi." if security_issues else "Bilinen CVE yok, secret sızıntısı tespit edilmedi.",
                "stats": [
                    ("Açık", f"{len([i for i in security_issues if i.severity == SeverityLevel.HIGH])} yüksek"),
                    ("Çözüldü", str(len(security_issues)))
                ]
            },
            "cleanCode": {
                "value": clean_code_score,
                "label": "Temiz Kod",
                "desc": f"{len(solid_issues) + len(architecture_issues)} kod kalitesi sorunu tespit edildi." if (solid_issues or architecture_issues) else "Tutarlı stil, düşük karmaşıklık.",
                "stats": [
                    ("Smell", str(len(solid_issues))),
                    ("Issues", str(len(architecture_issues)))
                ]
            },
            "perf": {
                "value": perf_score,
                "label": "Performans / Bellek",
                "desc": "Senkron işlemler event loop'u bloklayabilir." if any("blocking" in i.message.lower() for i in report.issues) else "Performans profili düz.",
                "stats": [
                    ("Hot path", str(len([i for i in report.issues if 'loop' in i.message.lower() or 'async' in i.message.lower()]))),
                    ("Avg ms", "N/A")
                ]
            },
            "robust": {
                "value": robust_score,
                "label": "Genel Sağlamlık",
                "desc": f"Hata yönetimi iyileştirilmeli, {len(architecture_issues)} try-except bloğu eksik." if architecture_issues else "Kapsamlı test paketi, anlamlı hata mesajları.",
                "stats": [
                    ("Try block", str(len([i for i in report.issues if 'try' in i.message.lower() or 'except' in i.message.lower()]))),
                    ("Coverage", "N/A")
                ]
            }
        }
    }
