
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator



class Settings(BaseSettings):
    PROJECT_NAME: str = 'scholarly-api'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:80", "https://localhost:80", "http://localhost:8000", "https://localhost:8000","http://localhost:3000", "https://localhost:3000", "http://localhost", "https://localhost"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_prefix = 'SCHOLARLY_'
        fields = {
            'PROJECT_NAME': {
                'env': 'PROJECT_NAME',
            },
            'BACKEND_CORS_ORIGINS': {
                'env': 'BACKEND_CORS_ORIGINS'
            }
        }


settings = Settings()
