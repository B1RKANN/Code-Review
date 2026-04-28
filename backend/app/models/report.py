from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime
from app.schemas.analysis import AnalysisReport

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.any_schema()

class ReportInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    file_name: str
    report_data: AnalysisReport
    llm_suggestions: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
