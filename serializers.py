from pydantic import BaseModel

class UrlShortnerSerializer(BaseModel):
    url: str

class ShortnerResultSerializer(BaseModel):
    long_url: str
    short_url: str
    is_cached: bool = False
    host_name: str