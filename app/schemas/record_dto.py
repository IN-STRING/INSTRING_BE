from pydantic import BaseModel

class RecordCreateRequest(BaseModel):
    name: str
    file_url: str
    spec_img_url: str

class RecordGetRequest(BaseModel):
    id: int
    name: str

class SearchRecords(BaseModel):
    records: list[RecordGetRequest]

class ChangeRecord(BaseModel):
    name: str