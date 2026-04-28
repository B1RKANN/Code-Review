import ast
from typing import List, Type
from app.analyzers.base import BaseAnalyzer
from app.analyzers.solid import SRPAnalyzer
from app.analyzers.security import SecurityAnalyzer
from app.schemas.analysis import CodeIssue, AnalysisReport

class AnalysisEngine:
    """
    Verilen Python kaynak kodunu AST'ye çevirip kayıtlı tüm analizörleri
    sırasıyla çalıştıran ana motor.
    """
    def __init__(self):
        # Çalıştırılacak analizörlerin listesi
        self.analyzers: List[Type[BaseAnalyzer]] = [
            SRPAnalyzer,
            SecurityAnalyzer
        ]

    def analyze_code(self, source_code: str, file_name: str = "unknown.py") -> AnalysisReport:
        issues: List[CodeIssue] = []
        
        try:
            # Kodu AST ağacına dönüştür
            tree = ast.parse(source_code)
            
            # Her bir analizörü çalıştır
            for AnalyzerClass in self.analyzers:
                analyzer_instance = AnalyzerClass(source_code)
                analyzer_instance.visit(tree)
                issues.extend(analyzer_instance.get_results())
                
        except SyntaxError as e:
            # Kod geçerli bir Python kodu değilse
            issues.append(
                CodeIssue(
                    category="Architecture",
                    severity="High",
                    line_number=e.lineno or 1,
                    message=f"Sözdizimi hatası (Syntax Error): {e.msg}",
                    code_snippet=e.text.strip() if e.text else ""
                )
            )
        except Exception as e:
            # Beklenmeyen diğer hatalar
            issues.append(
                CodeIssue(
                    category="Architecture",
                    severity="High",
                    line_number=1,
                    message=f"Analiz sırasında beklenmeyen bir hata oluştu: {str(e)}",
                )
            )

        return AnalysisReport(
            file_name=file_name,
            issues=issues,
            total_issues=len(issues)
        )
