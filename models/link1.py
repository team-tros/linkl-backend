from pydantic import BaseModel


class GetLink(BaseModel):
    link: str


