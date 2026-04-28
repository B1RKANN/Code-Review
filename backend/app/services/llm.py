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
        
    async def generate_suggestions(self, source_code: str, report: AnalysisReport) -> str:
        """
        AST motorundan çıkan analiz raporunu ve kaynak kodu OpenAI'a göndererek
        çözüm önerileri alır.
        """
        if not self.client:
            return "LLM sağlayıcısı (OpenAI API Key) yapılandırılmadığı için AI önerileri alınamıyor."
            
        if report.total_issues == 0:
            return "Harika kod! AST analiz motoru herhangi bir SOLID, Mimari veya Güvenlik ihlali tespit etmedi."

        # Rapor detaylarını prompt'a uygun formata çevir
        issues_text = ""
        for i, issue in enumerate(report.issues, 1):
            issues_text += f"{i}. Satır {issue.line_number} [{issue.category} - {issue.severity}]: {issue.message}\n"
            if issue.code_snippet:
                issues_text += f"   Sorunlu Kod: `{issue.code_snippet}`\n"

        prompt = f"""
Sen uzman bir Python Yazılım Mimarı ve Güvenlik Uzmanısın. Clean Code, SOLID prensipleri ve güvenli kodlama konularında derin bilgiye sahipsin.
Aşağıdaki Python kodu üzerinde bir AST analiz motoru çalıştırıldı ve bazı ihlaller tespit edildi.

Görevlerin:
1. Tespit edilen sorunların neden kötü bir pratik (anti-pattern) olduğunu kısaca açıkla.
2. Bu sorunları çözmek için kodun nasıl yeniden düzenlenmesi (refactoring) gerektiğini gösteren geliştirilmiş kod örnekleri sun.

[KAYNAK KOD]:
```python
{source_code}
```

[AST ANALİZ MOTORU BULGULARI]:
{issues_text}

Lütfen Türkçe olarak profesyonel ve eğitici bir dille yanıt ver.
"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Veya "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "Sen kıdemli bir Python yazılım mimarısın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3, # Daha deterministik (mantıklı) kodlar için düşük sıcaklık
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM önerisi alınırken bir hata oluştu: {str(e)}"
