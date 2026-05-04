import ast
from typing import List
from app.analyzers.base import BaseAnalyzer
from app.schemas.analysis import CodeIssue, Category, SeverityLevel

class SecurityAnalyzer(BaseAnalyzer):
    """
    Temel güvenlik ihlallerini kontrol eder:
    - exec() veya eval() kullanımı (Arbitrary code execution)
    - Hardcoded şifreler veya gizli anahtarlar
    """
    
    DANGEROUS_FUNCTIONS = {"eval", "exec"}
    SUSPICIOUS_VAR_NAMES = {"password", "secret", "api_key", "token"}

    def visit_Call(self, node: ast.Call):
        # exec() veya eval() çağrılarını kontrol et
        if isinstance(node.func, ast.Name):
            if node.func.id in self.DANGEROUS_FUNCTIONS:
                self.issues.append(
                    CodeIssue(
                        category=Category.SECURITY,
                        severity=SeverityLevel.HIGH,
                        line_number=node.lineno,
                        message=f"Tehlikeli fonksiyon kullanımı tespit edildi: '{node.func.id}()'. Bu durum kod enjeksiyonu zafiyetine yol açabilir.",
                        code_snippet=self.get_snippet(node.lineno)
                    )
                )
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        # Hardcoded şifre kontrolü
        # Örn: password = "my_super_secret_password" veya user, password = ("admin", "123")
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            for target in node.targets:
                self._check_target_for_secrets(target, node.lineno)
        elif isinstance(node.value, ast.Tuple) or isinstance(node.value, ast.List):
            # Tuple/List unpacking durumu için elemanları kontrol et
            for target in node.targets:
                if isinstance(target, ast.Tuple) or isinstance(target, ast.List):
                    for el in target.elts:
                        self._check_target_for_secrets(el, node.lineno)

        self.generic_visit(node)

    def _check_target_for_secrets(self, target: ast.AST, lineno: int):
        if isinstance(target, ast.Name):
            var_name = target.id.lower()
            if any(suspicious in var_name for suspicious in self.SUSPICIOUS_VAR_NAMES):
                self.issues.append(
                    CodeIssue(
                        category=Category.SECURITY,
                        severity=SeverityLevel.HIGH,
                        line_number=lineno,
                        message=f"Olası hardcoded gizli bilgi tespit edildi: '{target.id}'. Hassas verileri çevre değişkenleri (environment variables) ile yönetin.",
                        code_snippet=self.get_snippet(lineno)
                    )
                )

    def get_results(self) -> List[CodeIssue]:
        return self.issues
