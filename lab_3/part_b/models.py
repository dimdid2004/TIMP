from pydantic import BaseModel

class UserRegister(BaseModel):
    user_agent: str
    os: str
    cores: int
    graphical_inf: str