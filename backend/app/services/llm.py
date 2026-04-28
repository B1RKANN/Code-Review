from openai import AsyncOpenAI
from app.core.config import settings
from app.schemas.analysis import AnalysisReport

class LLMService:
    """
    OpenAI API ile etkileşime girerek AST analiz sonuçları ve kaynak kod
    üzerinden refactoring (iyileştirme) önerileri üreten servis.
    """
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
        
    async def generate_suggestions(self, source_code: str, report: AnalysisReport, language: str = "python") -> str:
        """
        AST motorundan çıkan analiz raporunu ve kaynak kodu OpenAI'a göndererek
        çözüm önerileri alır.
        """
        if not self.client:
            return "LLM sağlayıcısı (OpenAI API Key) yapılandırılmadığı için AI önerileri alınamıyor."

        if report.total_issues == 0 and language == "python":
            return "Harika kod! Analiz motoru herhangi bir SOLID, Mimari veya Güvenlik ihlali tespit etmedi."

        issues_text = ""
        has_issues = len(report.issues) > 0
        for i, issue in enumerate(report.issues, 1):
            issues_text += f"{i}. Satır {issue.line_number} [{issue.category} - {issue.severity}]: {issue.message}\n"
            if issue.code_snippet:
                issues_text += f"   Sorunlu Kod:\n```{language}\n{issue.code_snippet}\n```\n"

        lang_display = {
            "python": "Python", "javascript": "JavaScript", "typescript": "TypeScript",
            "java": "Java", "go": "Go", "rust": "Rust", "csharp": "C#",
            "cpp": "C++", "c": "C", "ruby": "Ruby", "php": "PHP"
        }.get(language, language.upper())

        if has_issues:
            prompt = f"""
Sen uzman bir {lang_display} Yazılım Mimarısın. Clean Code, SOLID prensipleri ve güvenli kodlama konularında derin bilgiye sahipsin.
Aşağıdaki {lang_display} kodu üzerinde bir analiz motoru çalıştırıldı ve bazı ihlaller tespit edildi.

Görevlerin:
1. Tespit edilen sorunların neden kötü bir pratik (anti-pattern) olduğunu kısaca açıkla.
2. Bu sorunları çözmek için kodun nasıl yeniden düzenlenmesi (refactoring) gerektiğini gösteren geliştirilmiş kod örnekleri sun.

[KAYNAK KOD]:
```{language}
{source_code}
```

[ANALİZ MOTORU BULGULARI]:
{issues_text}

Lütfen Türkçe olarak profesyonel ve eğitici bir dille yanıt ver.
"""
        else:
            prompt = f"""
Sen uzman bir {lang_display} Yazılım Mimarısın. Clean Code, SOLID prensipleri ve güvenli kodlama konularında derin bilgiye sahipsin.
Aşağıdaki {lang_display} kodunu incele ve aşağıdaki açılardan değerlendir:
1. SOLID prensiplerine uygunluk
2. Potansiyel güvenlik açıkları
3. Genel kod kalitesi ve iyileştirme önerileri

[BOLUM - KAYNAK KOD]:
```{language}
{source_code}
```

Lütfen Türkçe olarak profesyonel ve eğitici bir dille yanıt ver. Eğer kodta herhangi bir sorun yoksa, bu kodun iyi yönlerini belirt.
"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"Sen kıdemli bir {lang_display} yazılım mimarısın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM önerisi alınırken bir hata oluştu: {str(e)}"