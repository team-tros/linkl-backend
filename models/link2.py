from pydantic import BaseModel


class CrateLink(BaseModel):
    link: str
    redirect_link: str
