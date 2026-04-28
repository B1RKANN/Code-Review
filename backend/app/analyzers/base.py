import ast
from abc import ABC, abstractmethod
from typing import List
from app.schemas.analysis import CodeIssue

class BaseAnalyzer(ast.NodeVisitor, ABC):
    """
    Tüm AST analizörleri için temel sınıf.
    ast.NodeVisitor sınıfını miras alır, böylece AST ağacını gezebiliriz.
    """
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lines = source_code.splitlines()
        self.issues: List[CodeIssue] = []

    def get_snippet(self, lineno: int) -> str:
        """İlgili satırın kodunu döndürür."""
        if 0 < lineno <= len(self.lines):
            return self.lines[lineno - 1].strip()
        return ""

    @abstractmethod
    def get_results(self) -> List[CodeIssue]:
        """Bulunan sorunları döndürür."""
        pass
