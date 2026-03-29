from pydantic import BaseModel


class Email(BaseModel):
    email: str

class Password(BaseModel):
    password: str

class UserJoinDTO(Email):
    password: str

class VerifyDTO(Email):
    otp: str

class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str

class TempToken(BaseModel):
    temp_token: str
    token_type: str