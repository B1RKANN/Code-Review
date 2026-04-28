from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Category(str, Enum):
    SOLID = "SOLID"
    ARCHITECTURE = "Architecture"
    SECURITY = "Security"

class CodeIssue(BaseModel):
    category: Category
    severity: SeverityLevel
    line_number: int
    message: str
    code_snippet: Optional[str] = None
    suggestion: Optional[str] = None

class AnalysisReport(BaseModel):
    file_name: str
    issues: List[CodeIssue]
    total_issues: int
