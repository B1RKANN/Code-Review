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


class MetricStat(BaseModel):
    label: str
    value: str


class FileMetric(BaseModel):
    value: int
    label: str
    desc: str
    stats: List[tuple[str, str]]


class FileScore(BaseModel):
    overall: int
    status: str
    statusKind: str
    metrics: dict[str, FileMetric]


class Finding(BaseModel):
    sev: str
    title: str
    loc: str
    tag: str


class Aside(BaseModel):
    sev: str
    line: int
    title: str
    desc: str
    fix: Optional[str] = None


class FileAnalysisResult(BaseModel):
    score: FileScore
    findings: List[Finding]
    sources: List[tuple[int, str, Optional[str]]]
    aside: List[Aside]


class ProjectScores(BaseModel):
    files: dict[str, FileScore]

