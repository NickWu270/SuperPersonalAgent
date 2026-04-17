from pydantic import BaseModel, Field


class BoChaSearchInput(BaseModel):
    query: str = Field(..., description="搜索查询内容")
