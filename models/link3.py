from pydantic import BaseModel


class GetLinkinfo(BaseModel):
    link: str
