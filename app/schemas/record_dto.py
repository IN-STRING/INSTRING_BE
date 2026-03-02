from pydantic import BaseModel

class RecordCreateRequest(BaseModel):
    name: str
    style: str
    chord: str
    speed: str
    file_url: str
    spec_img_url: str

class RecordGetRequest(RecordCreateRequest):
    id: int

class SearchRecords(BaseModel):
    records: list[RecordGetRequest]