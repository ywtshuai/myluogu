from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Neo4j FastAPI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Database REST API for ai_world"
    API_V1_STR: str = "/api/v1"

    NEO4J_URI: str = "neo4j://1.12.255.121:7687/"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "aw_neo4j_123456"
    NEO4J_PASSWORD: str

    REDIS_URL: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"


settings = Settings()