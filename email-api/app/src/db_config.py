from pydantic import BaseSettings, Field


class DBSettings(BaseSettings):
    DB_USERNAME: str = Field(env='DB_USERNAME')
    DB_PASSWORD: str = Field(env='DB_PASSWORD')
    DB_DATABASE: str = Field(env='DB_NAME')
    DB_HOST: str = Field(env='DB_HOST')
    DB_PORT: int = Field(env='DB_PORT')

    @property
    def data_source_name(self):
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"


db_settings = DBSettings()
