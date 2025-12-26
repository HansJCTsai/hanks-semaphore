import json
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# 設定 config.json 的路徑
CONFIG_JSON_PATH = Path("config.json")


def load_json_config() -> Dict[str, Any]:
    """讀取 config.json 並轉換為 Settings 需要的格式"""
    if not CONFIG_JSON_PATH.exists():
        print(
            f"Warning: {CONFIG_JSON_PATH} not found, relying on environment variables."
        )
        return {}

    with open(CONFIG_JSON_PATH, encoding="utf-8") as f:
        try:
            data = json.load(f)
            postgres = data.get("postgres", {})

            return {
                "POSTGRES_SERVER": postgres.get("host"),
                "POSTGRES_USER": postgres.get("user"),
                "POSTGRES_PASSWORD": postgres.get("pass"),
                "POSTGRES_DB": postgres.get("name"),
                "POSTGRES_PORT": str(postgres.get("port", 5432)),
            }
        except json.JSONDecodeError:
            print("Error: Failed to decode config.json")
            return {}


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hanks Semaphore API"
    API_V1_STR: str = "/api/v1"

    # [新增 1] 定義這些欄位，因為環境變數或 config 裡有它們
    SECRET_KEY: str = "dev-secret-key-change-me"
    DATABASE_URL: Optional[str] = None

    # 資料庫相關設定
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: str = "5432"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # 如果環境變數已經給了完整的 DATABASE_URL，就直接用
        if self.DATABASE_URL:
            return self.DATABASE_URL

        # 否則就用各個參數組合成 Postgres 連線字串
        if (
            self.POSTGRES_SERVER
            and self.POSTGRES_USER
            and self.POSTGRES_PASSWORD
            and self.POSTGRES_DB
        ):
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

        # 如果都沒有，回傳一個預設值或是報錯 (這裡示範預設 sqlite)
        return "sqlite+aiosqlite:///./test.db"

    # [新增 2] Pydantic V2 設定：允許忽略多餘的環境變數 (extra="ignore")
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore",  # 關鍵：這樣就不會因為多餘的變數報錯了
    )


# 初始化
json_config = load_json_config()
settings = Settings(**json_config)
