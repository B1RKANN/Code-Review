import ast
from typing import List
from app.analyzers.base import BaseAnalyzer
from app.schemas.analysis import CodeIssue, Category, SeverityLevel

class SRPAnalyzer(BaseAnalyzer):
    """
    Single Responsibility Principle (Tek Sorumluluk Prensibi) kontrolü.
    - Çok fazla metoda sahip sınıfları (Örn: > 10 metot)
    - Çok uzun sınıfları veya metotları tespit eder.
    """
    
    MAX_METHODS_PER_CLASS = 10
    MAX_LINES_PER_CLASS = 200
    MAX_LINES_PER_METHOD = 50

    def visit_ClassDef(self, node: ast.ClassDef):
        # Sınıfın metodlarını bul
        methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        
        # 1. Metot sayısı kontrolü
        if len(methods) > self.MAX_METHODS_PER_CLASS:
            self.issues.append(
                CodeIssue(
                    category=Category.SOLID,
                    severity=SeverityLevel.MEDIUM,
                    line_number=node.lineno,
                    message=f"Sınıf '{node.name}' çok fazla metoda sahip ({len(methods)}). SRP ihlali olabilir.",
                    code_snippet=self.get_snippet(node.lineno)
                )
            )

        # 2. Sınıf satır sayısı kontrolü
        if hasattr(node, 'end_lineno') and node.end_lineno:
            class_length = node.end_lineno - node.lineno
            if class_length > self.MAX_LINES_PER_CLASS:
                self.issues.append(
                    CodeIssue(
                        category=Category.SOLID,
                        severity=SeverityLevel.MEDIUM,
                        line_number=node.lineno,
                        message=f"Sınıf '{node.name}' çok uzun ({class_length} satır). Sınıfı bölmeyi düşünün.",
                        code_snippet=self.get_snippet(node.lineno)
                    )
                )

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._check_function_length(node)
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._check_function_length(node)
        self.generic_visit(node)

    def _check_function_length(self, node: ast.AST):
        if hasattr(node, 'end_lineno') and node.end_lineno:
            func_length = node.end_lineno - node.lineno
            if func_length > self.MAX_LINES_PER_METHOD:
                self.issues.append(
                    CodeIssue(
                        category=Category.SOLID,
                        severity=SeverityLevel.MEDIUM,
                        line_number=node.lineno,
                        message=f"Metot '{node.name}' çok uzun ({func_length} satır). Metodu alt fonksiyonlara bölmeyi düşünün.",
                        code_snippet=self.get_snippet(node.lineno)
                    )
                )

    def get_results(self) -> List[CodeIssue]:
        return self.issues
