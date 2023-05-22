from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    class Config:
        env_file=".env"

settings=Settings()

class Credidentials(BaseSettings):
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    MAIL_SERVER:str
    MAIL_PORT:int

    class Config:
        env_file=".env"

credidentials=Credidentials()
