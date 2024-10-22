from pydantic import BaseModel, ConfigDict
from typing import Optional

class TasksData(BaseModel):
    id: Optional[int] = None
    task: str